from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r"^api/health$", views.health),
    re_path(r"^api/agents$", views.agents_list),
    re_path(r"^api/settings$", views.settings_view),
    re_path(r"^api/resumes/upload$", views.resumes_upload),
    re_path(r"^api/resumes$", views.resumes_view),
    re_path(r"^api/resumes/(?P<rid>[0-9a-f]+)$", views.resume_delete),
    re_path(r"^api/jobs$", views.jobs_view),
    re_path(r"^api/jobs/(?P<jid>[0-9a-f]+)$", views.job_delete),
    re_path(r"^api/match$", views.match),
    re_path(r"^api/demo/load$", views.demo_load),
    re_path(r"^api/reextract$", views.reextract),
    re_path(r"^api/reset$", views.reset),
    re_path(r"^assets/(?P<path>.*)$", views.serve_assets),
    re_path(r"^.*$", views.index),
]
