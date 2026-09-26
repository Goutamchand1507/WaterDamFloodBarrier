from django.contrib import admin
from django.urls import path
from django.shortcuts import render

from estimation.views import (
    calculate_estimation,
    estimation_history,
    estimation_report,
    delete_estimation,
    edit_estimation,
    dashboard,
    compare_estimations,
)

from projects.views import (
    project_list,
    add_project,
    edit_project,
    delete_project,
    project_summary,
)

from materials.views import (
    material_list,
    add_material,
    edit_material,
    delete_material,
)


# ============================================================
# HOME PAGE
# ============================================================

def home(request):

    return render(
        request,
        "home.html"
    )


# ============================================================
# URL PATTERNS
# ============================================================

urlpatterns = [

    # --------------------------------------------------------
    # HOME
    # --------------------------------------------------------

    path(
        "",
        home,
        name="home"
    ),


    # --------------------------------------------------------
    # ADMIN
    # --------------------------------------------------------

    path(
        "admin/",
        admin.site.urls
    ),


    # --------------------------------------------------------
    # ESTIMATION
    # --------------------------------------------------------

    path(
        "estimation/",
        calculate_estimation,
        name="estimation"
    ),


    # --------------------------------------------------------
    # ESTIMATION HISTORY
    # --------------------------------------------------------

    path(
        "history/",
        estimation_history,
        name="history"
    ),


    # --------------------------------------------------------
    # ESTIMATION REPORT
    # --------------------------------------------------------

    path(
        "report/<int:estimation_id>/",
        estimation_report,
        name="estimation_report"
    ),


    # --------------------------------------------------------
    # DELETE ESTIMATION
    # --------------------------------------------------------

    path(
        "delete-estimation/<int:estimation_id>/",
        delete_estimation,
        name="delete_estimation"
    ),


    # --------------------------------------------------------
    # EDIT ESTIMATION
    # --------------------------------------------------------

    path(
        "edit-estimation/<int:estimation_id>/",
        edit_estimation,
        name="edit_estimation"
    ),


    # --------------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------------

    path(
        "dashboard/",
        dashboard,
        name="dashboard"
    ),


    # --------------------------------------------------------
    # COMPARE ESTIMATIONS
    # --------------------------------------------------------

    path(
        "compare/",
        compare_estimations,
        name="compare_estimations"
    ),


    # ========================================================
    # PROJECTS
    # ========================================================

    path(
        "projects/",
        project_list,
        name="projects"
    ),


    # --------------------------------------------------------
    # ADD PROJECT
    # --------------------------------------------------------

    path(
        "projects/add/",
        add_project,
        name="add_project"
    ),


    # --------------------------------------------------------
    # EDIT PROJECT
    # --------------------------------------------------------

    path(
        "projects/edit/<int:project_id>/",
        edit_project,
        name="edit_project"
    ),


    # --------------------------------------------------------
    # DELETE PROJECT
    # --------------------------------------------------------

    path(
        "projects/delete/<int:project_id>/",
        delete_project,
        name="delete_project"
    ),


    # --------------------------------------------------------
    # PROJECT SUMMARY
    # --------------------------------------------------------

    path(
        "projects/summary/<int:project_id>/",
        project_summary,
        name="project_summary"
    ),


    # ========================================================
    # MATERIALS
    # ========================================================

    path(
        "materials/",
        material_list,
        name="materials"
    ),


    # --------------------------------------------------------
    # ADD MATERIAL
    # --------------------------------------------------------

    path(
        "materials/add/",
        add_material,
        name="add_material"
    ),


    # --------------------------------------------------------
    # EDIT MATERIAL
    # --------------------------------------------------------

    path(
        "materials/edit/<int:material_id>/",
        edit_material,
        name="edit_material"
    ),


    # --------------------------------------------------------
    # DELETE MATERIAL
    # --------------------------------------------------------

    path(
        "materials/delete/<int:material_id>/",
        delete_material,
        name="delete_material"
    ),

]