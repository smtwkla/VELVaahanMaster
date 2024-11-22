import frappe
import os
from frappe.utils.data import get_url
from frappe.utils import get_files_path


def write_file(file):
	"""
		Override default file upload behavior
	"""
	attached_doc_type = file.attached_to_doctype
	doctype_folder = attached_doc_type.lower().replace(" ", "_")

	if file.is_private:
		create_folder = f'{frappe.utils.get_site_base_path()}/private/files/{doctype_folder}'
		file.file_url = f'/private/files/{doctype_folder}/{file.file_name}'
	else:
		create_folder = f'{frappe.utils.get_site_base_path()}/public/files/{doctype_folder}'
		file.file_url = f'/files/{doctype_folder}/{file.file_name}'

	try:
		os.mkdir(create_folder)
	except FileExistsError:
		pass

	fpath = file.write_file()
	return {"file_name": os.path.basename(fpath), "file_url": file.file_url}
