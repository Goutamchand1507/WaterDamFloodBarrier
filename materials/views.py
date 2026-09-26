from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Material


def material_list(request):
    search = request.GET.get("search", "")

    materials = Material.objects.all().order_by("material_name")

    if search:
        materials = materials.filter(
            material_name__icontains=search
        )

    return render(
        request,
        "materials/material_list.html",
        {
            "materials": materials,
            "search": search,
        },
    )


def add_material(request):
    error = None

    if request.method == "POST":
        try:
            material_name = request.POST.get(
                "material_name", ""
            ).strip()

            density = float(
                request.POST.get("density", "")
            )

            unit = request.POST.get(
                "unit", ""
            ).strip()

            unit_price = float(
                request.POST.get("unit_price", "")
            )

            # Basic validation

            if not material_name:
                raise ValueError(
                    "Material name is required."
                )

            if not unit:
                raise ValueError(
                    "Unit is required."
                )

            if density <= 0:
                raise ValueError(
                    "Density must be greater than zero."
                )

            if unit_price < 0:
                raise ValueError(
                    "Unit price cannot be negative."
                )

            # Realistic-value validation

            if density > 100000:
                raise ValueError(
                    "Density value is unrealistic."
                )

            if unit_price > 10000000:
                raise ValueError(
                    "Unit price value is unrealistic."
                )

            # Duplicate material validation

            if Material.objects.filter(
                material_name__iexact=material_name
            ).exists():

                raise ValueError(
                    "A material with this name already exists."
                )

            # Create material

            Material.objects.create(
                material_name=material_name,
                density=density,
                unit=unit,
                unit_price=unit_price,
            )

            messages.success(
                request,
                f"Material '{material_name}' added successfully!"
            )

            return redirect("materials")

        except ValueError as e:

            error = str(e)

        except Exception as e:

            error = f"Something went wrong: {e}"

    return render(
        request,
        "materials/add_material.html",
        {
            "error": error,
        },
    )


def edit_material(request, material_id):

    material = get_object_or_404(
        Material,
        id=material_id
    )

    error = None

    if request.method == "POST":

        try:

            material_name = request.POST.get(
                "material_name", ""
            ).strip()

            density = float(
                request.POST.get("density", "")
            )

            unit = request.POST.get(
                "unit", ""
            ).strip()

            unit_price = float(
                request.POST.get("unit_price", "")
            )

            # Basic validation

            if not material_name:
                raise ValueError(
                    "Material name is required."
                )

            if not unit:
                raise ValueError(
                    "Unit is required."
                )

            if density <= 0:
                raise ValueError(
                    "Density must be greater than zero."
                )

            if unit_price < 0:
                raise ValueError(
                    "Unit price cannot be negative."
                )

            # Realistic-value validation

            if density > 100000:
                raise ValueError(
                    "Density value is unrealistic."
                )

            if unit_price > 10000000:
                raise ValueError(
                    "Unit price value is unrealistic."
                )

            # Duplicate material validation
            # Exclude the material currently being edited

            duplicate_exists = Material.objects.filter(
                material_name__iexact=material_name
            ).exclude(
                id=material.id
            ).exists()

            if duplicate_exists:

                raise ValueError(
                    "Another material with this name already exists."
                )

            # Update material

            material.material_name = material_name
            material.density = density
            material.unit = unit
            material.unit_price = unit_price

            material.save()

            messages.success(
                request,
                f"Material '{material_name}' updated successfully!"
            )

            return redirect("materials")

        except ValueError as e:

            error = str(e)

        except Exception as e:

            error = f"Something went wrong: {e}"

    return render(
        request,
        "materials/edit_material.html",
        {
            "material": material,
            "error": error,
        },
    )


def delete_material(request, material_id):

    material = get_object_or_404(
        Material,
        id=material_id
    )

    if request.method == "POST":

        material_name = material.material_name

        material.delete()

        messages.success(
            request,
            f"Material '{material_name}' deleted successfully!"
        )

        return redirect("materials")

    return render(
        request,
        "materials/delete_material.html",
        {
            "material": material,
        },
    )