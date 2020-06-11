from django.urls import path

from . import views

urlpatterns = [
    #     path('', views.index, name='index'),
    path("", views.IngredientListView.as_view(), name="ingredient_list"),
    path("add/", views.IngredientAddView.as_view(), name="ingredient_add"),
    path(
        "add/modal/",
        views.IngredientModalAddView.as_view(),
        name="ingredient_add_modal",
    ),
    path(
        "add/modal/submit/",
        views.IngredientModalAddView.as_view(partial=True),
        name="ingredient_add_modal_submit",
    ),
    path(
        "<int:ingredient_id>/",
        views.IngredientUpdateView.as_view(),
        name="ingredient_update",
    ),
    path("unit/", views.MeasureUnitListView.as_view(), name="unit_list"),
    path("unit/add/", views.MeasureUnitAddView.as_view(), name="unit_add"),
    path(
        "unit_group/", views.MeasureUnitGroupListView.as_view(), name="unit_group_list"
    ),
    path(
        "unit_group/add/",
        views.MeasureUnitGroupAddView.as_view(),
        name="unit_group_add",
    ),
    path(
        "unit_group/<int:unit_group_id>/",
        views.MeasureUnitGroupUpdateView.as_view(),
        name="unit_group_update",
    ),
]
