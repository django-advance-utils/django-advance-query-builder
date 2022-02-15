from django.urls import path

from advanced_report_builder.views.bar_charts import BarChartModal, BarChartFieldModal
from advanced_report_builder.views.dashboard import DashboardReportModal, DashboardModal, DashboardAddReportModal
from advanced_report_builder.views.datatables.modal import TableModal, TableFieldModal, TablePivotModal
from advanced_report_builder.views.funnel_charts import FunnelChartModal, FunnelChartFieldModal
from advanced_report_builder.views.kanban import KanbanModal, KanbanLaneModal
from advanced_report_builder.views.line_charts import LineChartModal, LineChartFieldModal
from advanced_report_builder.views.pie_charts import PieChartModal, PieChartFieldModal
from advanced_report_builder.views.reports import DuplicateReportModal
from advanced_report_builder.views.single_values import SingleValueModal, ShowBreakdownModal
from advanced_report_builder.views.targets.views import TargetModal

app_name = 'advanced_report_builder'


urlpatterns = [
    path('table/modal/<str:slug>/', TableModal.as_view(), name='table_modal'),
    path('table/modal/field/<str:slug>/', TableFieldModal.as_view(), name='table_field_modal'),
    path('table/modal/pivot/<str:slug>/', TablePivotModal.as_view(), name='table_pivot_modal'),

    path('single-value/modal/<str:slug>/', SingleValueModal.as_view(), name='single_value_modal'),
    path('single-value/show-breakdown/<str:slug>/', ShowBreakdownModal.as_view(), name='show_breakdown_modal'),

    path('bar-chart/modal/<str:slug>/', BarChartModal.as_view(), name='bar_chart_modal'),
    path('bar-chart/modal/field/<str:slug>/', BarChartFieldModal.as_view(), name='bar_chart_field_modal'),

    path('line-chart/modal/<str:slug>/', LineChartModal.as_view(), name='line_chart_modal'),
    path('line-chart/modal/field/<str:slug>/', LineChartFieldModal.as_view(), name='line_chart_field_modal'),

    path('pie-chart/modal/<str:slug>/', PieChartModal.as_view(), name='pie_chart_modal'),
    path('pie-chart/modal/field/<str:slug>/', PieChartFieldModal.as_view(), name='pie_chart_field_modal'),

    path('funnel-chart/modal/<str:slug>/', FunnelChartModal.as_view(), name='funnel_chart_modal'),
    path('funnel-chart/modal/field/<str:slug>/', FunnelChartFieldModal.as_view(), name='funnel_chart_field_modal'),

    path('kanban/modal/<str:slug>/', KanbanModal.as_view(), name='kanban_modal'),
    path('kanban/modal/lane/<str:slug>/', KanbanLaneModal.as_view(), name='kanban_lane_modal'),

    path('dashboard/report/<str:slug>/', DashboardReportModal.as_view(), name='dashboard_report_modal'),
    path('dashboard/<str:slug>/', DashboardModal.as_view(), name='dashboard_modal'),
    path('dashboard/add/<str:slug>/', DashboardAddReportModal.as_view(), name='add_dashboard_report'),

    path('duplicate/<str:slug>/', DuplicateReportModal.as_view(), name='duplicate_report_modal'),

    path('target/modal/<str:slug>/', TargetModal.as_view(), name='target_modal'),

]
