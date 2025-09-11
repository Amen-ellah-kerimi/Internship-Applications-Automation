from flask import Flask

def register_routes(app: Flask):
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
            new_candidates = services.scrape_and_save_candidates()
            flash(f"{new_candidates} new candidates added.", "success")
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
                request.form.get("folder")
            )
            flash("Settings updated successfully.", "success")
            return redirect(url_for("settings"))
        return render_template("settings.html", setting=setting)

