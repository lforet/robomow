from robomow_relay_class import *


relay = robomow_relay("/dev/ttyACM0")
print relay.stats()

print "turning relay 1 on"
relay.turn_relay_1_on()
print relay.get_relay_states()
time.sleep(1)
print "turning relay 1 off"
relay.turn_relay_1_off()
print relay.get_relay_states()
time.sleep(1)

print "turning relay 2 on"
relay.turn_relay_2_on()
print relay.get_relay_states()
time.sleep(1)
print "turning relay 2 off"
relay.turn_relay_2_off()
print relay.get_relay_states()
time.sleep(1)

print "turning both relays on"
relay.turn_relay_1_on()
relay.turn_relay_2_on()
print relay.get_relay_states()
time.sleep(1)
print "turning both relays off"
relay.turn_relay_1_off()
relay.turn_relay_2_off()
print relay.get_relay_states()
time.sleep(1)

print "relay.relay1_state:", relay.relay1_state
print "relay.relay2_state:", relay.relay2_state

print "performing rapid power cycles"
for i in range (5):
	relay.turn_relay_1_on()
	time.sleep(.1)
	relay.turn_relay_2_on()
	time.sleep(.1)
	print relay.get_relay_states()
	relay.turn_relay_1_off()
	time.sleep(.1)
	relay.turn_relay_2_off()
	print relay.get_relay_states()
	time.sleep(.1)
for i in range (5):
	print relay.get_relay_states()
	relay.turn_relay_1_on()
	relay.turn_relay_2_on()
	time.sleep(.1)
	print relay.get_relay_states()
	relay.turn_relay_1_off()
	relay.turn_relay_2_off()
	time.sleep(.1)




