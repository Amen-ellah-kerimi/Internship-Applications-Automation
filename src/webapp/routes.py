from flask import Flask

def register_routes(app: Flask):
    # -------------------------
    # Serve files from attachements folder
    # -------------------------
    @app.route('/attachements/<filename>')
    def download_attachment(filename):
        from flask import send_from_directory
        attachments_dir = '/home/amen/stage/career/attachements'
        return send_from_directory(attachments_dir, filename, as_attachment=True)
    # -------------------------
    # View Attachment
    # -------------------------
    @app.route("/attachment/<int:attachment_id>")
    def view_attachment(attachment_id):
        from src.webapp.models import Attachment
        from flask import send_file, abort
        import os
        att = Attachment.query.get_or_404(attachment_id)
        abs_path = os.path.abspath(os.path.join('/home/amen/stage/career/attachements', att.filename))
        if not os.path.exists(abs_path):
            return abort(404)
        return send_file(abs_path)
    # -------------------------
    # Mark Candidate as Reviewed
    # -------------------------
    @app.route("/candidate/<int:candidate_id>/toggle_reviewed", methods=["POST"])
    def toggle_reviewed(candidate_id):
        from src.webapp.models import Candidate
        from src.webapp.app import db
        candidate = Candidate.query.get_or_404(candidate_id)
        candidate.read = not candidate.read
        db.session.commit()
        flash(f"Candidate '{candidate.name}' marked as {'reviewed' if candidate.read else 'not reviewed'}.", "success")
        return redirect(url_for("dashboard"))
    import src.webapp.services as services
    from src.webapp.models import Candidate
    from flask import render_template, request, redirect, url_for, flash

    # -------------------------
    # Dashboard
    # -------------------------
    @app.route("/", methods=["GET", "POST"])
    def dashboard():
        if request.method == "POST":
            # Scrape button clicked
                result = services.scrape_and_save_candidates()
                if isinstance(result, dict) and result.get("error"):
                    flash(result["error"], "danger")
                else:
                    count = result.get("new_count", 0) if isinstance(result, dict) else 0
                    flash(f"{count} new candidates added.", "success")
                return redirect(url_for("dashboard"))

        candidates = Candidate.query.order_by(Candidate.applied_on.desc()).all()
        return render_template("dashboard.html", candidates=candidates)


    # -------------------------
    # Candidate Detail
    # -------------------------
    @app.route("/candidate/<int:candidate_id>")
    def candidate_detail(candidate_id):
        candidate, attachments = services.get_candidate_details(candidate_id)
        return render_template("candidate_detail.html", candidate=candidate, attachments=attachments)


    # -------------------------
    # Settings
    # -------------------------
    @app.route("/settings", methods=["GET", "POST"])
    def settings():
        setting = services.get_settings()
        if request.method == "POST":
            services.update_settings(
                request.form.get("imap_server"),
                request.form.get("email_user"),
                request.form.get("email_pass"),
                request.form.get("folder"),
                request.form.get("attachment_folder"),
                request.form.get("internship_code_map")
            )
            flash("Settings updated successfully.", "success")
            return redirect(url_for("settings"))
        return render_template("settings.html", setting=setting)

