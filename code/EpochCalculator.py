import datetime

# Get the current date in UTC
current_date_utc = datetime.datetime.utcnow().date()

# Define the start and end of the day in UTC
start_of_day_utc = datetime.datetime.combine(current_date_utc, datetime.time.min)
end_of_day_utc = datetime.datetime.combine(current_date_utc, datetime.time.max)

# print("Start of the day (UTC):", start_of_day_utc)
# print("End of the day (UTC):", end_of_day_utc)

# Convert to Unix timestamps (Epoch)
epoch_start_of_day_utc = int(start_of_day_utc.timestamp())
epoch_end_of_day_utc = int(end_of_day_utc.timestamp())

# print("Epoch for the start of the day (UTC):", epoch_start_of_day_utc)
# print("Epoch for the end of the day (UTC):", epoch_end_of_day_utc)