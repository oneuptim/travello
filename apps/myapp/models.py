from __future__ import unicode_literals
from django.db import models
import re, bcrypt

passRegex = re.compile(r'^(?=.{8,15}$)(?=.*[A-Z])(?=.*[0-9]).*$')
emailRegex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
nameRegex = re.compile(r'^(?=.{2,})([a-zA-z]*)$')

class UserManager(models.Manager):

	def register(self, first_name, last_name, email, password, confirm_password ):
		errors = []
		if (len(first_name) == 0) or (len(last_name) == 0)  or (len(email) == 0) or (len(password) == 0):
			errors.append("Cannot be blank")

		if ((not nameRegex.match(first_name)) or (not nameRegex.match(last_name)) ):
		# elif (not emailRegex.match(email)) or (not nameRegex.match(first_name)) or (not nameRegex.match(last_name)):
			errors.append("Name must be at least 2 characters with no letters...")


		if (not emailRegex.match(email)):
			errors.append("Invalid email ....")

		else:

			email_registeres = User.objects.filter(email=email)
			print email_registeres,
			if (email_registeres):
				if (email==email_registeres[0].email):
					errors.append("Email exits in our system ")



		if (not passRegex.match(password)):
			errors.append("Password be at 8-15 characters with one capital letter...")

		if (not (password == confirm_password)):
			errors.append("Password don't match")


		if len(errors) is not 0:
			return (False, errors)
		else:
			pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
			print pw_hash, "888888888888888"
			new_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)

		return (True, new_user)

	def login(self, email, password):
		errors =[]

		user = User.objects.filter(email=email)
		# This query returns as an array, should always be unwrapped/unzipped in order to access the objects in the array!

		if user:
			print user,"user exist", user[0].password
			compare_password = password.encode()
			if bcrypt.hashpw(compare_password, user[0].password.encode()) == user[0].password:
			# if (user[0].password == password):
				print user[0].password,"That is your password"

				return (True, user)
			else:
				errors.append("password didnt match")
				print "password didnt match"
				return (False, errors)
		else:
			print "no email found"
			errors.append("No email found in our system, please register dude!!!")
			return (False, errors)

class TripManager(models.Manager):
	def add_trip(self, post, session):

		error = []
		destination = post['destination']
		description = post['description']
		start_date = post["start_date"]
		end_date = post ['end_date']

		if (len(destination) == 0) or (len(description) == 0) or (len(start_date) == 0) or (len(end_date) == 0):
			errors.append("Cannot be blank")
		else:
			user = User.objects.get(id=session)
			# print user
			new_trip_object = Trip.objects.create(destination=destination, description=description, start_date=start_date, end_date=end_date, participant=user)
			print new_trip_object
			return (new_trip_object)

	def join_trip(self, session, id):
		participant = User.objects.filter(id=session)[0]
		tripObject = Trip.objects.filter(id=id)[0] # Returns an object

		print participant.first_name, tripObject.id, "%"*200

		joined_trip = Schedule.objects.create(participant=participant, trip=tripObject)

		return(joined_trip)

	def hide_joined_trip(self, session, id):
		participant_id = User.objects.get(id=session)
		# trip_id = Trip.objects.get(trip.id=id)
		# trip_in_schedule_id = Schedule.objects.get(trip.id=id)

		print participant_id

		# , "Trip ID:" trip_id, "Schedule ID:" trip_in_schedule_id, "%"*100


		# if trip.id == trip.trip.id and trip.participant.id == session:
		# 	all_trips_minus_joined_trips = all_trips.exclude(id=6).order_by('-created_at')
		#
		# 	all_trips_list = Trip.objects.exclude(participant_id=participant_id)


class User(models.Model):
	first_name = models.CharField(max_length=45, blank=True, null=True)
	last_name = models.CharField(max_length=45, blank=True, null=True)
	email = models.EmailField(max_length = 255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

			# -----login/registration------

class Trip(models.Model):
	destination = models.CharField(max_length=100, null=True)
	description = models.CharField(max_length=1000, null=True)
	start_date=models.DateTimeField(null=True)
	end_date=models.DateTimeField(null=True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	participant = models.ForeignKey('User', null=True, related_name="tripparticipant")
	objects = TripManager()
	# class Meta:
	# 	unique_together= (('user', 'participant'),)


class Schedule(models.Model):
	participant = models.ForeignKey('User', null=True, related_name ="participantschedule") # null=True was not set, same way it's set in Trip so migrations wouldn't run. That's why field wasn't beeing populated.
	trip = models.ForeignKey('Trip', related_name ="tripschedule")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = TripManager()
