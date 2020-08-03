from pubsub import pub

# The listeners for these topics must accept the listed key arg, if any (or **kwargs)
REFRESH_BUTTON_CLICKED = "RREFRESH_BUTTON_CLICKED"
DETAILS_WINDOW_CLOSED = "DETAILS_WINDOW_CLOSED"
NOTIFICATION_CREATED = "NOTIFICATION_CREATED"   # key arg: text (str), mode (str), page (str)
DATABASE_MODIFIED = "DATABASE_MODIFIED"

# Any call to pub.sendMessage / pub.subscribe will be done through these functions instead. To make it easier to disable
# the functionality while pypubsub get installed on mygeohub.
unsubAll = pub.unsubAll
sendMessage = pub.sendMessage
subscribe = pub.subscribe
