import krpc
import time
import math as ma
import numpy as np

conn = krpc.connect(name='Mission Control')
KSC = conn.space_center
vessel = KSC.active_vessel
print("")
print(f"Mission Control is online!")

vo = vessel.orbit
vc = vessel.control
ap = vessel.auto_pilot
v_ref = vessel.reference_frame
s_ref = vessel.surface_reference_frame
sv_ref = vessel.surface_velocity_reference_frame
vob_ref = vessel.orbit.body.reference_frame
cd = conn.drawing
# initial launchpad position vector
posV = np.matrix([vessel.position(vob_ref)])

# helpers
stream = conn.add_stream
ap = vessel.auto_pilot
control = vessel.control
orbit = vessel.orbit
orbital_body = vessel.orbit.body
flight = vessel.flight
call = conn.get_call
fuel_amount = vessel.resources.amount
bodies = conn.space_center.bodies
tgt_pitch_heading = ap.target_pitch_and_heading

# reference frames
RF = vessel.reference_frame
orbital_RF = vessel.orbital_reference_frame
nr_orbital_RF = vessel.orbit.body.non_rotating_reference_frame
surface_RF = vessel.surface_reference_frame
create_hybrid = conn.space_center.ReferenceFrame.create_hybrid
surface_vel_RF = create_hybrid(position=orbital_RF, rotation=surface_RF)

# in-game time
ut = stream(getattr, KSC, 'ut')
met = stream(getattr, vessel, 'met')

# position
position = stream(vessel.position, orbit.body.reference_frame)

# vessel
mass = stream(getattr, vessel, 'mass')
dry_mass = stream(getattr, vessel, 'dry_mass')
crew_capacity = stream(getattr, vessel, 'crew_capacity')
crew_count = stream(getattr, vessel, 'crew_count')
crew = stream(getattr, vessel, 'crew')
current_biome = stream(getattr, vessel, 'biome')

# resources
SF_amt = call(fuel_amount, 'SolidFuel')
LF_amt = call(fuel_amount, 'LiquidFuel')
OX_amt = call(fuel_amount, 'Oxidizer')
MP_amt = call(fuel_amount, 'MonoPropellant')

# vessel engines
engine = vessel.parts.engines[0]
engine_is_active = stream(getattr, engine, 'active')
thrust = stream(getattr, engine, 'thrust')
available_thrust = stream(getattr, engine, 'available_thrust')
max_thrust_asl = stream(getattr, engine, 'max_thrust')
max_thrust_vac = stream(getattr, engine, 'max_vacuum_thrust')
Isp_asl = stream(getattr, engine, 'kerbin_sea_level_specific_impulse')
Isp = stream(getattr, engine, 'specific_impulse')
Isp_vac = stream(getattr, engine, 'vacuum_specific_impulse')
fuel_types = stream(getattr, engine, 'propellant_names')
fuel_ratio = stream(getattr, engine, 'propellant_ratios')
got_fuel = stream(getattr, engine, 'has_fuel')
throttle = stream(getattr, engine, 'throttle')

# surface data
current_biome = stream(getattr, vessel, 'biome')

# surface flight
altitude = stream(getattr, flight(surface_RF), 'mean_altitude')
surface_speed = stream(getattr, flight(surface_RF), 'speed')
surface_vel = stream(getattr, flight(surface_vel_RF), 'velocity')
vert_speed = stream(getattr, flight(surface_RF), 'vertical_speed')
slip_angle = stream(getattr, flight(surface_RF), 'sideslip_angle')
static_temp = stream(getattr, flight(surface_RF), 'static_air_temperature')
pitch = stream(getattr, flight(surface_RF), 'pitch')
heading = stream(getattr, flight(surface_RF), 'heading')
roll = stream(getattr, flight(surface_RF), 'roll')
aoa = stream(getattr, flight(surface_RF), 'angle_of_attack')
p_atmo = stream(getattr, flight(surface_RF), 'atmosphere_density')
q = stream(getattr, flight(surface_RF), 'dynamic_pressure')
g_force = stream(getattr, flight(surface_RF), 'g_force')
v_terminal = stream(getattr, flight(surface_RF), 'terminal_velocity')
static_temp = stream(getattr, flight(surface_RF), 'static_air_temperature')

# orbital flight
orbital_speed = stream(getattr, flight(orbital_RF), 'speed')
apoapsis = stream(getattr, orbit, 'apoapsis_altitude')
time_to_apo = stream(getattr, orbit, 'time_to_apoapsis')
periapsis = stream(getattr, orbit, 'periapsis_altitude')
time_to_pe = stream(getattr, orbit, 'time_to_periapsis')
inclination = stream(getattr, orbit, 'inclination')
ecc = stream(getattr, orbit, 'eccentricity')

# celestial body info




# ---------------------------------------------------------------------------- #
# -- Telemetry methods -- #

def get_attitude():
    return f"pitch,heading,roll: {pitch()}, {heading()}, {slip_angle()}"

# Basic vector operations

def mag(v):
    """magnitude of a vector"""
    return np.linalg.norm(v)

def dot_p(u, v):
    """ method 1 for dot product calculation to find angle  """
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]

def cross_p(u, v):
    """ returns the cross product of two vectors u x v - orthogonal to u and v """
    return (u[1]*v[2] - u[2]*v[1],
            u[2]*v[0] - u[0]*v[2],
            u[0]*v[1] - u[1]*v[0])

def UV_theta(u, v):
    """ returns angle between vectors, checks if they are parallel """
    dotp = dot_p(u, v)
    theta = ma.acos(dotp / (mag(u) * mag(v))) * (180/ma.pi)
    return theta

def g_turn(initial_alt,final_alt):
    """Gravity turn method"""
    theta0 = 0
    h0 = initial_alt
    hf = final_alt
    if altitude() > h0 and altitude() < hf:
        frac = ((altitude()-h0) / (hf - h0)) 
        theta = frac*90
        if abs(theta - theta0) > 0.5:
            theta0 = theta
            tgt_pitch_heading(90-theta0,90)
