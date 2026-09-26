from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Estimation
from projects.models import Project
from materials.models import Material


# ---------------------------------------------------------
# NEW ESTIMATION
# ---------------------------------------------------------

def calculate_estimation(request):

    projects = Project.objects.all()
    materials = Material.objects.all()

    result = None
    error = None

    if request.method == "POST":

        try:
            project_id = request.POST.get("project")
            material_id = request.POST.get("material")

            water_level = float(request.POST.get("water_level"))
            ground_level = float(request.POST.get("ground_level"))
            safety_allowance = float(request.POST.get("safety_allowance"))

            barrier_length = float(request.POST.get("barrier_length"))
            barrier_width = float(request.POST.get("barrier_width"))

            labour_cost = float(request.POST.get("labour_cost") or 0)
            equipment_cost = float(request.POST.get("equipment_cost") or 0)
            transportation_cost = float(
                request.POST.get("transportation_cost") or 0
            )
            other_cost = float(request.POST.get("other_cost") or 0)

            project = get_object_or_404(Project, id=project_id)
            material = get_object_or_404(Material, id=material_id)

            # -------------------------------------------------
            # VALIDATION
            # -------------------------------------------------

            if water_level < 0:
                raise ValueError("Water level cannot be negative.")

            if ground_level < 0:
                raise ValueError("Ground level cannot be negative.")

            if safety_allowance < 0:
                raise ValueError("Safety allowance cannot be negative.")

            if barrier_length <= 0:
                raise ValueError("Barrier length must be greater than zero.")

            if barrier_width <= 0:
                raise ValueError("Barrier width must be greater than zero.")

            if material.density <= 0:
                raise ValueError("Material density must be greater than zero.")

            if material.unit_price < 0:
                raise ValueError("Material price cannot be negative.")

            if labour_cost < 0:
                raise ValueError("Labour cost cannot be negative.")

            if equipment_cost < 0:
                raise ValueError("Equipment cost cannot be negative.")

            if transportation_cost < 0:
                raise ValueError(
                    "Transportation cost cannot be negative."
                )

            if other_cost < 0:
                raise ValueError("Other cost cannot be negative.")

            if water_level > 1000:
                raise ValueError("Water level value is unrealistic.")

            if ground_level > 1000:
                raise ValueError("Ground level value is unrealistic.")

            if safety_allowance > 100:
                raise ValueError(
                    "Safety allowance value is unrealistic."
                )

            if barrier_length > 100000:
                raise ValueError(
                    "Barrier length value is unrealistic."
                )

            if barrier_width > 1000:
                raise ValueError(
                    "Barrier width value is unrealistic."
                )

            if water_level < ground_level:
                raise ValueError(
                    "Water level should be greater than or equal to "
                    "ground level."
                )

            # -------------------------------------------------
            # CALCULATIONS
            # -------------------------------------------------

            barrier_height = (
                water_level
                - ground_level
                + safety_allowance
            )

            if barrier_height <= 0:
                raise ValueError(
                    "Calculated barrier height must be greater than zero."
                )

            if barrier_height > 1000:
                raise ValueError(
                    "Calculated barrier height is unrealistic."
                )

            barrier_volume = (
                barrier_length
                * barrier_width
                * barrier_height
            )

            material_quantity = (
                barrier_volume
                * material.density
            )

            material_cost = (
                material_quantity
                * material.unit_price
            )

            total_cost = (
                material_cost
                + labour_cost
                + equipment_cost
                + transportation_cost
                + other_cost
            )

            # -------------------------------------------------
            # SAVE ESTIMATION
            # -------------------------------------------------

            estimation = Estimation.objects.create(
                project=project,
                material=material,

                water_level=water_level,
                ground_level=ground_level,
                safety_allowance=safety_allowance,

                barrier_length=barrier_length,
                barrier_width=barrier_width,
                barrier_height=barrier_height,
                barrier_volume=barrier_volume,

                material_quantity=material_quantity,
                material_cost=material_cost,

                labour_cost=labour_cost,
                equipment_cost=equipment_cost,
                transportation_cost=transportation_cost,
                other_cost=other_cost,

                total_cost=total_cost,
            )

            return redirect(
                "estimation_report",
                estimation_id=estimation.id
            )

        except ValueError as e:
            error = str(e)

        except Exception as e:
            error = f"Something went wrong: {e}"

    return render(
        request,
        "estimation/estimation_form.html",
        {
            "projects": projects,
            "materials": materials,
            "result": result,
            "error": error,
        },
    )


# ---------------------------------------------------------
# ESTIMATION HISTORY
# ---------------------------------------------------------

def estimation_history(request):

    search = request.GET.get("search", "")

    estimations = Estimation.objects.select_related(
        "project",
        "material"
    ).order_by("-created_date")

    if search:
        estimations = estimations.filter(
            project__project_name__icontains=search
        ) | estimations.filter(
            material__material_name__icontains=search
        )

    return render(
        request,
        "estimation/history.html",
        {
            "estimations": estimations,
            "search": search,
        },
    )


# ---------------------------------------------------------
# ESTIMATION REPORT
# ---------------------------------------------------------

def estimation_report(request, estimation_id):

    estimation = get_object_or_404(
        Estimation.objects.select_related(
            "project",
            "material"
        ),
        id=estimation_id,
    )

    return render(
        request,
        "estimation/report.html",
        {
            "estimation": estimation,
        },
    )


# ---------------------------------------------------------
# DELETE ESTIMATION
# ---------------------------------------------------------

def delete_estimation(request, estimation_id):

    estimation = get_object_or_404(
        Estimation,
        id=estimation_id
    )

    if request.method == "POST":

        estimation.delete()

        messages.success(
            request,
            "Estimation deleted successfully!"
        )

        return redirect("history")

    return render(
        request,
        "estimation/delete_estimation.html",
        {
            "estimation": estimation,
        },
    )


# ---------------------------------------------------------
# EDIT ESTIMATION
# ---------------------------------------------------------

def edit_estimation(request, estimation_id):

    estimation = get_object_or_404(
        Estimation,
        id=estimation_id
    )

    projects = Project.objects.all()
    materials = Material.objects.all()

    error = None

    if request.method == "POST":

        try:

            project_id = request.POST.get("project")
            material_id = request.POST.get("material")

            water_level = float(
                request.POST.get("water_level")
            )

            ground_level = float(
                request.POST.get("ground_level")
            )

            safety_allowance = float(
                request.POST.get("safety_allowance")
            )

            barrier_length = float(
                request.POST.get("barrier_length")
            )

            barrier_width = float(
                request.POST.get("barrier_width")
            )

            labour_cost = float(
                request.POST.get("labour_cost") or 0
            )

            equipment_cost = float(
                request.POST.get("equipment_cost") or 0
            )

            transportation_cost = float(
                request.POST.get("transportation_cost") or 0
            )

            other_cost = float(
                request.POST.get("other_cost") or 0
            )

            project = get_object_or_404(
                Project,
                id=project_id
            )

            material = get_object_or_404(
                Material,
                id=material_id
            )

            # -------------------------------------------------
            # VALIDATION
            # -------------------------------------------------

            if water_level < 0:
                raise ValueError(
                    "Water level cannot be negative."
                )

            if ground_level < 0:
                raise ValueError(
                    "Ground level cannot be negative."
                )

            if safety_allowance < 0:
                raise ValueError(
                    "Safety allowance cannot be negative."
                )

            if barrier_length <= 0:
                raise ValueError(
                    "Barrier length must be greater than zero."
                )

            if barrier_width <= 0:
                raise ValueError(
                    "Barrier width must be greater than zero."
                )

            if material.density <= 0:
                raise ValueError(
                    "Material density must be greater than zero."
                )

            if material.unit_price < 0:
                raise ValueError(
                    "Material price cannot be negative."
                )

            if labour_cost < 0:
                raise ValueError(
                    "Labour cost cannot be negative."
                )

            if equipment_cost < 0:
                raise ValueError(
                    "Equipment cost cannot be negative."
                )

            if transportation_cost < 0:
                raise ValueError(
                    "Transportation cost cannot be negative."
                )

            if other_cost < 0:
                raise ValueError(
                    "Other cost cannot be negative."
                )

            if water_level > 1000:
                raise ValueError(
                    "Water level value is unrealistic."
                )

            if ground_level > 1000:
                raise ValueError(
                    "Ground level value is unrealistic."
                )

            if safety_allowance > 100:
                raise ValueError(
                    "Safety allowance value is unrealistic."
                )

            if barrier_length > 100000:
                raise ValueError(
                    "Barrier length value is unrealistic."
                )

            if barrier_width > 1000:
                raise ValueError(
                    "Barrier width value is unrealistic."
                )

            if water_level < ground_level:
                raise ValueError(
                    "Water level should be greater than or equal "
                    "to ground level."
                )

            # -------------------------------------------------
            # RECALCULATE VALUES
            # -------------------------------------------------

            barrier_height = (
                water_level
                - ground_level
                + safety_allowance
            )

            if barrier_height <= 0:
                raise ValueError(
                    "Calculated barrier height must be greater "
                    "than zero."
                )

            if barrier_height > 1000:
                raise ValueError(
                    "Calculated barrier height is unrealistic."
                )

            barrier_volume = (
                barrier_length
                * barrier_width
                * barrier_height
            )

            material_quantity = (
                barrier_volume
                * material.density
            )

            material_cost = (
                material_quantity
                * material.unit_price
            )

            total_cost = (
                material_cost
                + labour_cost
                + equipment_cost
                + transportation_cost
                + other_cost
            )

            # -------------------------------------------------
            # UPDATE EXISTING ESTIMATION
            # -------------------------------------------------

            estimation.project = project
            estimation.material = material

            estimation.water_level = water_level
            estimation.ground_level = ground_level
            estimation.safety_allowance = safety_allowance

            estimation.barrier_length = barrier_length
            estimation.barrier_width = barrier_width
            estimation.barrier_height = barrier_height
            estimation.barrier_volume = barrier_volume

            estimation.material_quantity = material_quantity
            estimation.material_cost = material_cost

            estimation.labour_cost = labour_cost
            estimation.equipment_cost = equipment_cost
            estimation.transportation_cost = transportation_cost
            estimation.other_cost = other_cost

            estimation.total_cost = total_cost

            estimation.save()

            # SUCCESS MESSAGE

            messages.success(
                request,
                "Estimation updated successfully!"
            )

            return redirect(
                "estimation_report",
                estimation_id=estimation.id
            )

        except ValueError as e:

            error = str(e)

        except Exception as e:

            error = f"Something went wrong: {e}"

    return render(
        request,
        "estimation/edit_estimation.html",
        {
            "estimation": estimation,
            "projects": projects,
            "materials": materials,
            "error": error,
        },
    )


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

def dashboard(request):

    total_estimations = Estimation.objects.count()
    total_projects = Project.objects.count()
    total_materials = Material.objects.count()

    total_estimated_cost = sum(
        estimation.total_cost
        for estimation in Estimation.objects.all()
    )

    average_estimation_cost = 0

    if total_estimations > 0:
        average_estimation_cost = (
            total_estimated_cost
            / total_estimations
        )

    recent_estimations = Estimation.objects.select_related(
        "project",
        "material"
    ).order_by("-created_date")[:5]

    return render(
        request,
        "estimation/dashboard.html",
        {
            "total_estimations": total_estimations,
            "total_projects": total_projects,
            "total_materials": total_materials,
            "total_estimated_cost": total_estimated_cost,
            "average_estimation_cost": average_estimation_cost,
            "recent_estimations": recent_estimations,
        },
    )


# ---------------------------------------------------------
# COMPARE ESTIMATIONS
# ---------------------------------------------------------

def compare_estimations(request):

    selected_ids = request.GET.getlist("estimation_ids")

    comparison_error = None
    estimations = []

    if selected_ids:

        if len(selected_ids) < 2:

            comparison_error = (
                "Please select at least two estimations "
                "to compare."
            )

        else:

            estimations = Estimation.objects.select_related(
                "project",
                "material"
            ).filter(
                id__in=selected_ids
            )

            if estimations.count() < 2:

                comparison_error = (
                    "Please select at least two valid "
                    "estimations."
                )

    return render(
        request,
        "estimation/compare.html",
        {
            "estimations": estimations,
            "comparison_error": comparison_error,
        },
    )