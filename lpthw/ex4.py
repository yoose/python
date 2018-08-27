# this defines the number of cars available
cars = 100
# this defines the number of spaces per car
space_in_a_car = 4.0
# this defines the number of drivers available
drivers = 30
# this defines the number of passengers that need a ride
passengers = 90
# this defines the number of cars that do not have a driver
cars_not_driven = cars - drivers
# this sets the number of cars driven equal to the number of drivers available
cars_driven = drivers
# this defines the total number of spaces available for carpool
carpool_capacity = cars_driven * space_in_a_car
# this defines the average number of passengers there will be per car
average_passengers_per_car = passengers / cars_driven


print("There are", cars, "cars available")
print("There are only", drivers, "drivers available.")
print("There will be", cars_not_driven, "empty cars today.")
print("We can transport", carpool_capacity, "people today.")
print("We have", passengers, "to carpool today.")
print("We need to put about", average_passengers_per_car, "in each car.")
