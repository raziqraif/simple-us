from pubsub import pub

REFRESH_BUTTON_CLICKED = "RREFRESH_BUTTON_CLICKED"


# Any call to pub.sendMessage / pub.subscribe will be done through these functions instead. To make it easier to disable
# the functionality while pypubsub get installed on mygeohub.
unsubAll = pub.unsubAll
sendMessage = pub.sendMessage
subscribe = pub.subscribe
