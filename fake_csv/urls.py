from django.urls import path

from .views import (
    CustomLoginView,
    CustomLogoutView,
    SchemaListView,
    SchemaDeleteView,
    SchemaUpdateView,
    SchemaCreateView,
    SchemaDetailView,
    CreateDataset,
    UpdateDatasetStatus,
    DeleteColumnView,
)

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("", SchemaListView.as_view(), name="schema_list"),
    path("create_schema/", SchemaCreateView.as_view(), name="create_schema"),
    path("detail_schema/<int:pk>/", SchemaDetailView.as_view(), name="detail_schema"),
    path("update_schema/<int:pk>/", SchemaUpdateView.as_view(), name="update_schema"),
    path("delete_schema/<int:pk>/", SchemaDeleteView.as_view(), name="delete_schema"),
    path("delete_column/<int:pk>/", DeleteColumnView.as_view(), name="delete_column"),
    path("create_dataset/", CreateDataset.as_view(), name="create_dataset"),
    path(
        "update_dataset_status/",
        UpdateDatasetStatus.as_view(),
        name="update_dataset_status",
    ),
]
