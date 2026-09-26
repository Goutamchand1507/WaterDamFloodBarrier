from django.shortcuts import render, get_object_or_404, redirect
import json

from .models import Project
from estimation.models import Estimation


# ============================================================
# PROJECT LIST
# ============================================================

def project_list(request):

    projects = (
        Project.objects.all()
        .order_by("-created_date")
    )

    return render(
        request,
        "projects/project_list.html",
        {
            "projects": projects,
        },
    )


# ============================================================
# ADD PROJECT
# ============================================================

def add_project(request):

    if request.method == "POST":

        project_name = request.POST.get(
            "project_name"
        )

        location = request.POST.get(
            "location"
        )

        if project_name and location:

            Project.objects.create(
                project_name=project_name,
                location=location,
            )

            return redirect("projects")

    return render(
        request,
        "projects/add_project.html"
    )


# ============================================================
# EDIT PROJECT
# ============================================================

def edit_project(
    request,
    project_id
):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    if request.method == "POST":

        project_name = request.POST.get(
            "project_name"
        )

        location = request.POST.get(
            "location"
        )

        if project_name and location:

            project.project_name = project_name
            project.location = location

            project.save()

            return redirect("projects")

    return render(
        request,
        "projects/edit_project.html",
        {
            "project": project,
        },
    )


# ============================================================
# DELETE PROJECT
# ============================================================

def delete_project(
    request,
    project_id
):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    if request.method == "POST":

        project.delete()

        return redirect("projects")

    return render(
        request,
        "projects/delete_project.html",
        {
            "project": project,
        },
    )


# ============================================================
# PROJECT SUMMARY
# ============================================================

def project_summary(
    request,
    project_id
):

    project = get_object_or_404(
        Project,
        id=project_id
    )


    # ========================================================
    # GET PROJECT ESTIMATIONS
    # ========================================================

    estimations = (
        Estimation.objects
        .filter(
            project=project
        )
        .order_by(
            "-created_date"
        )
    )


    # ========================================================
    # TOTAL ESTIMATIONS
    # ========================================================

    total_estimations = (
        estimations.count()
    )


    # ========================================================
    # TOTAL ESTIMATED COST
    # ========================================================

    total_estimated_cost = sum(
        estimation.total_cost
        for estimation in estimations
    )


    # ========================================================
    # AVERAGE ESTIMATED COST
    # ========================================================

    average_estimated_cost = 0

    if total_estimations > 0:

        average_estimated_cost = (
            total_estimated_cost
            /
            total_estimations
        )


    # ========================================================
    # LATEST ESTIMATION
    # ========================================================

    latest_estimation = None

    if estimations.exists():

        latest_estimation = (
            estimations.first()
        )


    # ========================================================
    # MATERIAL SUMMARY
    # ========================================================

    material_summary = {}


    for estimation in estimations:

        material_name = (
            estimation.material.material_name
        )


        if material_name not in material_summary:

            material_summary[material_name] = {

                "quantity": 0,

                "cost": 0,

            }


        material_summary[
            material_name
        ]["quantity"] += (
            estimation.material_quantity
        )


        material_summary[
            material_name
        ]["cost"] += (
            estimation.material_cost
        )


    # ========================================================
    # CONVERT MATERIAL SUMMARY TO LIST
    # ========================================================

    material_summary_list = []


    for material_name, values in (
        material_summary.items()
    ):

        material_summary_list.append(

            {

                "material_name":
                    material_name,

                "quantity":
                    values["quantity"],

                "cost":
                    values["cost"],

            }

        )


    # ========================================================
    # COST BREAKDOWN
    # ========================================================

    total_material_cost = sum(
        estimation.material_cost
        for estimation in estimations
    )


    total_labour_cost = sum(
        estimation.labour_cost
        for estimation in estimations
    )


    total_equipment_cost = sum(
        estimation.equipment_cost
        for estimation in estimations
    )


    total_transportation_cost = sum(
        estimation.transportation_cost
        for estimation in estimations
    )


    total_other_cost = sum(
        estimation.other_cost
        for estimation in estimations
    )


    # ========================================================
    # COST CHART DATA
    # ========================================================

    cost_chart = [

        {
            "name": "Material",
            "cost": total_material_cost,
        },

        {
            "name": "Labour",
            "cost": total_labour_cost,
        },

        {
            "name": "Equipment",
            "cost": total_equipment_cost,
        },

        {
            "name": "Transportation",
            "cost": total_transportation_cost,
        },

        {
            "name": "Other",
            "cost": total_other_cost,
        },

    ]


    # ========================================================
    # CONVERT CHART DATA TO JSON
    # ========================================================

    cost_chart_json = json.dumps(
        cost_chart
    )


    # ========================================================
    # SEND DATA TO TEMPLATE
    # ========================================================

    return render(

        request,

        "projects/project_summary.html",

        {

            "project":
                project,

            "estimations":
                estimations,

            "total_estimations":
                total_estimations,

            "total_estimated_cost":
                total_estimated_cost,

            "average_estimated_cost":
                average_estimated_cost,

            "latest_estimation":
                latest_estimation,

            "material_summary":
                material_summary_list,

            "total_material_cost":
                total_material_cost,

            "total_labour_cost":
                total_labour_cost,

            "total_equipment_cost":
                total_equipment_cost,

            "total_transportation_cost":
                total_transportation_cost,

            "total_other_cost":
                total_other_cost,

            "cost_chart":
                cost_chart_json,

        },

    )