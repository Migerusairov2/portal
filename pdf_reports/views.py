from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.contrib.auth.models import User
from profile.models import Profile, Project, Trajectory
from collections import defaultdict
from textwrap import wrap



def pdf_report(request):

    user = User.objects.filter(is_superuser=True).first()

    if not user:
        return HttpResponse("No superuser found.")

    profile = Profile.objects.filter(user=user).first()

    projects = Project.objects.filter(user=user)
    trajectories = Trajectory.objects.filter(user=user)

    trainings = user.certificates.select_related('training').order_by('-issued_at')
    grouped_trainings = defaultdict(list)

    for cert in trainings:
        grouped_trainings[cert.training.source].append({
            'title': cert.training.title,
            'issued_at': cert.issued_at,
            'description': cert.training.description,
        })

    response = HttpResponse(content_type='application/pdf')
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()

    mobile_keywords = [
    'android',
    'iphone',
    'ipad',
    'ipod',
    'mobile'
    ]

    is_mobile = any(
    keyword in user_agent
    for keyword in mobile_keywords
)
    filename = "Miguel Angel C. Silos - CV.pdf"

    if is_mobile:
        response['Content-Disposition'] = (f'attachment; filename="{filename}"')
    else:
        response['Content-Disposition'] = (f'inline; filename="{filename}"')

    p = canvas.Canvas(response, pagesize=letter)

    width, height = letter

    # ==========================
    # MARGINS
    # ==========================

    LEFT_MARGIN = 30
    RIGHT_MARGIN = 30
    TOP_MARGIN = 30
    BOTTOM_MARGIN = 30

    y = height - TOP_MARGIN
    title_label = 10
    font_size = 9

    def new_page_if_needed(y_pos):
        if y_pos < BOTTOM_MARGIN:
            p.showPage()
            return height - TOP_MARGIN
        return y_pos

    # ==========================
    # HEADER
    # ==========================

    full_name = (
        f"{user.first_name or ''} "
        f"{user.last_name or ''}"
    ).strip()

    full_name = (
        f"{profile.first_name or ''} "
        f"{profile.middle_name[:1] or ''} {'.' if profile.middle_name else ''}"
        f"{profile.last_name or ''}"
    ).strip()

    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width / 2, y, full_name)

    y -= 25

    contact_info = (
        f"{user.email or ''}"
        f"{' | ' if profile.phone else ''}"
        f"{profile.phone if profile else ''}"
    )

    p.setFont("Helvetica", font_size)
    p.drawCentredString(width / 2, y, contact_info)

    y -= 15

    p.line(
        LEFT_MARGIN,
        y,
        width - RIGHT_MARGIN,
        y
    )

    y -= 20

    # ==========================
    # SUMMARY
    # ==========================

    p.setFont("Helvetica-Bold", title_label)
    p.drawString(
        LEFT_MARGIN,
        y,
        "PROFESSIONAL SUMMARY"
    )

    y -= 15

    p.setFont("Helvetica", font_size)

    description = (
        profile.description
        if profile and profile.description
        else ""
    )

    for line in wrap(description, width=130):
        y = new_page_if_needed(y)

        p.drawString(
            LEFT_MARGIN,
            y,
            line
        )

        y -= 14

    y -= 15

    # ==========================
    # EXPERIENCE
    # ==========================

    y = new_page_if_needed(y)

    p.setFont("Helvetica-Bold", title_label)
    p.drawString(
        LEFT_MARGIN,
        y,
        "EXPERIENCES"
    )

    y -= 15

    for trajectory in trajectories:

        y = new_page_if_needed(y)

        title = (
            f"{trajectory.job_position or ''}"
        )

        p.setFont("Helvetica-Bold", title_label)
        p.drawString(
            LEFT_MARGIN,
            y,
            title
        )


        dates = (
                f"{trajectory.date_start.strftime('%b %d, %Y') if trajectory.date_start else ''}"
                f" - "
                f"{trajectory.date_end.strftime('%b %d, %Y') if trajectory.date_end else 'Current'}"
            )

        p.setFont("Helvetica-Oblique", font_size)
        p.drawString(
            (width/2) + 175,
            y,
            dates
        )

        y -= 15

        p.setFont("Helvetica", font_size)

        for line in wrap(
            trajectory.description or "",
            width=130
        ):
            y = new_page_if_needed(y)

            p.drawString(
                LEFT_MARGIN + 15,
                y,
                line
            )

            y -= 12

        y -= 10

    # ==========================
    # PROJECTS
    # ==========================

    y = new_page_if_needed(y)

    p.setFont("Helvetica-Bold", title_label)
    p.drawString(
        LEFT_MARGIN,
        y,
        "PROJECTS"
    )

    y -= 20

    for project in projects:

        y = new_page_if_needed(y)

        p.setFont("Helvetica-Bold", title_label)

        p.drawString(
            LEFT_MARGIN,
            y,
            project.name or ""
        )

        y -= 15

        if hasattr(project, "description"):

            p.setFont("Helvetica", font_size)

            for line in wrap(
                project.description or "",
                width=130
            ):
                y = new_page_if_needed(y)

                p.drawString(
                    LEFT_MARGIN + 15,
                    y,
                    line
                )

                y -= 12

        y -= 10

    # ==========================
    # TRAININGS & CERTIFICATIONS
    # ==========================

    y = new_page_if_needed(y)

    p.setFont("Helvetica-Bold", title_label)
    p.drawString(
        LEFT_MARGIN,
        y,
        "TRAININGS & CERTIFICATIONS"
    )

    y -= 20

    for source, certificates in grouped_trainings.items():

        y = new_page_if_needed(y)

        p.setFont("Helvetica-Bold", font_size)
        p.drawString(
            LEFT_MARGIN,
            y,
            str(source)
        )

        y -= 15

        for cert in certificates:

            y = new_page_if_needed(y)

            p.setFont("Helvetica-Bold", font_size)

            title = cert["title"] or ""

            issued_at = (
                cert["issued_at"].strftime("%B %Y")
                if cert["issued_at"]
                else ""
            )

            p.drawString(
                LEFT_MARGIN + 10,
                y,
                f"• {title}"
            )

            y -= 12

            p.setFont("Helvetica-Oblique", font_size)

            p.drawString(
                LEFT_MARGIN + 25,
                y,
                f"Issued: {issued_at}"
            )

            y -= 12

            p.setFont("Helvetica", font_size)

            description = cert["description"] or ""

            for line in wrap(description, width=130):
                y = new_page_if_needed(y)

                p.drawString(
                    LEFT_MARGIN + 25,
                    y,
                    line
                )

                y -= 12

            y -= 10

        y -= 10


    # ==========================
    # FOOTER
    # ==========================

    p.setFont("Helvetica-Oblique", 8)

    p.drawCentredString(
        width / 2,
        30,
        "Generated from Django"
    )

    p.save()

    return response