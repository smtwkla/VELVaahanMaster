from idlelib.browser import file_open

import frappe
import os
from frappe.utils.data import get_url
from frappe.utils import get_files_path
from frappe.core.doctype.file.utils import generate_file_name, get_file_name
from frappe.utils.data import cstr


def write_file(file):
	"""
	Override default file upload behavior: upload files to separate folders named after doctype.
	Creates folder if it does not exist.
	If file already exists in folder, upload with random hash suffixed to file name.
	"""
	attached_doc_type = file.attached_to_doctype
	doctype_folder = attached_doc_type.lower().replace(" ", "_")
	base_path = frappe.utils.get_site_base_path()

	if file.is_private:
		create_folder = f'{base_path}/private/files/{doctype_folder}'
	else:
		create_folder = f'{base_path}/public/files/{doctype_folder}'

	try:
		os.mkdir(create_folder)
	except FileExistsError:
		pass
	except (PermissionError, FileNotFoundError) as e:
		frappe.throw("Unable to create folder {}".format(create_folder))

	filename_with_path = f'{create_folder}/{file.file_name}'
	if os.path.exists(filename_with_path):
		partial, extn = os.path.splitext(cstr(file.file_name))
		suffix = frappe.generate_hash(length=6)
		file.file_name = f"{partial}{suffix}{extn}"
	else:
		pass

	file.file_url = f'{"/private" if file.is_private else ""}/files/{doctype_folder}/{file.file_name}'

	fpath = file.write_file()
	return {"file_name": os.path.basename(fpath), "file_url": file.file_url}
