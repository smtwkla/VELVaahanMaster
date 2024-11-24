# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt
import json
import math
from pprint import pprint

import frappe
from frappe.model.document import Document


def haversine(lat1, lon1, lat2, lon2):
	"""
	Calculate the great-circle distance between two points on the Earth's surface.

	Parameters:
	- lat1, lon1: Latitude and Longitude of point 1 in decimal degrees
	- lat2, lon2: Latitude and Longitude of point 2 in decimal degrees

	Returns:
	- Distance in kilometers
	"""

	R = 6371.0  # Earth radius in kilometers

	lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

	dlat = lat2 - lat1
	dlon = lon2 - lon1
	a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

	return R * c

def is_within_radius(lat1, lon1, lat2, lon2, radius):
	"""
	Check if a point (lat2, lon2) is within a given radius from (lat1, lon1).

	Parameters:
	- lat1, lon1: Latitude and Longitude of the center point in decimal degrees
	- lat2, lon2: Latitude and Longitude of the point to check in decimal degrees
	- radius: Radius in kilometers

	Returns:
	- True if the point is within the radius, False otherwise
	"""

	distance = haversine(lat1, lon1, lat2, lon2)
	return distance <= radius


class VehicleRoute(Document):
	def set_title(self):
		self.title = f'{self.route_code}-{self.route_name}'

	def update_calculated_fields(self):
		self.stop_count = len(self.route_stops)
		if self.route_stops:
			self.total_km = self.route_stops[-1].km

	def check_if_pin_already_in_route(self, lat1, lon1):
		radius = .1
		for stop in self.route_stops:
			if is_within_radius(lat1, lon1, stop.latitude, stop.longitude, radius):
				return True
		return False

	def get_pins_from_map(self):
		map_data = json.loads(self.route_map)
		for feature in map_data['features']:
			if feature['geometry']['type'] == 'Point':
				pin = (feature['geometry']['coordinates'])
				if not self.check_if_pin_already_in_route(pin[0], pin[1]):
					new_pin = dict(stop_name="New", latitude=pin[0], longitude=pin[1], km=0)
					self.append("route_stops", new_pin)

	def before_save(self):
		self.set_title()
		self.update_calculated_fields()
		self.get_pins_from_map()

	def validate_segments(self):
		if not self.route_stops:
			frappe.throw("Please enter route stops.")

		last_km = None
		for s in self.route_stops:
			if last_km is None:
				if s.km != 0:
					frappe.throw("First stop is starting point and must have 0 km.")
			else:
				if s.km < last_km:
					frappe.throw("KM must be increasing: No.{}".format(s.idx))
			last_km = s.km

	def validate(self):
		self.validate_segments()
