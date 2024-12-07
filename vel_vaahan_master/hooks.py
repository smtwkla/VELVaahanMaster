app_name = "vel_vaahan_master"
app_title = "VEL Vaahan Master"
app_publisher = "SMTW"
app_description = "Vehicle Management ERP"
app_email = "kla@smtw.in"
app_license = "mit"
app_logo_url = "/assets/vel_vaahan_master/images/icon.svg"

write_file = "vel_vaahan_master.overrides.file_handler.write_file"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
add_to_apps_screen = [
	{
		"name": "vel_vaahan_master",
		"logo": "/assets/vel_vaahan_master/images/icon.svg",
		"title": "VEL Vaahan Master",
		"route": "/app/vel-vaahan-master" #,
		#"has_permission": "vel_vaahan_master.api.permission.has_app_permission"
	}
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/vel_vaahan_master/css/vel_vaahan_master.css"
app_include_js = "/assets/vel_vaahan_master/js/vel_vaahan_master.js"
# app_include_js = "/assets/vel_vaahan_master/js/map_defaults.js"
# include js, css files in header of web template
# web_include_css = "/assets/vel_vaahan_master/css/vel_vaahan_master.css"
# web_include_js = "/assets/vel_vaahan_master/js/vel_vaahan_master.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "vel_vaahan_master/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "vel_vaahan_master/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "vel_vaahan_master.utils.jinja_methods",
# 	"filters": "vel_vaahan_master.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "vel_vaahan_master.install.before_install"
# after_install = "vel_vaahan_master.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "vel_vaahan_master.uninstall.before_uninstall"
# after_uninstall = "vel_vaahan_master.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "vel_vaahan_master.utils.before_app_install"
# after_app_install = "vel_vaahan_master.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "vel_vaahan_master.utils.before_app_uninstall"
# after_app_uninstall = "vel_vaahan_master.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "vel_vaahan_master.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"after_insert": "",
# 	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"vel_vaahan_master.tasks.all"
# 	],
 	"daily": [
 		"vel_vaahan_master.vaahan.doctype.vaahan.tasks.daily",
	    "vel_vaahan_master.vehicle_operations.doctype.passenger_vehicle_trip.tasks.daily"
 	],
# 	"hourly": [
# 		"vel_vaahan_master.tasks.hourly"
# 	],
# 	"weekly": [
# 		"vel_vaahan_master.tasks.weekly"
# 	],
# 	"monthly": [
# 		"vel_vaahan_master.tasks.monthly"
# 	],
}

# Testing
# -------

# before_tests = "vel_vaahan_master.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "vel_vaahan_master.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "vel_vaahan_master.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["vel_vaahan_master.utils.before_request"]
# after_request = ["vel_vaahan_master.utils.after_request"]

# Job Events
# ----------
# before_job = ["vel_vaahan_master.utils.before_job"]
# after_job = ["vel_vaahan_master.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"vel_vaahan_master.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

