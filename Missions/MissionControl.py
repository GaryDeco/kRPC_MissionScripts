"""
-Mission Control module-
Contains streams and helpers for mission scripts

"""
import time
import math
import krpc


class HQ:
    """Superclass: HQ
    """

    def __init__(self):

        # setup
        self.conn = krpc.connect(name="Streams")
        self.KSC = self.conn.space_center
        self.vessel = self.KSC.active_vessel

        # helpers
        self.stream = self.conn.add_stream
        self.ap = self.vessel.auto_pilot
        self.control = self.vessel.control
        self.orbit = self.vessel.orbit
        self.orbital_body = self.vessel.orbit.body
        self.flight = self.vessel.flight
        self.call = self.conn.get_call
        self.fuel_amount = self.vessel.resources.amount
        self.bodies = self.conn.space_center.bodies

        # reference frames
        self.RF = self.vessel.reference_frame
        self.orbital_RF = self.vessel.orbital_reference_frame
        self.nr_orbital_RF = self.vessel.orbit.body.non_rotating_reference_frame
        self.surface_RF = self.vessel.surface_reference_frame
        self.create_hybrid = self.conn.space_center.ReferenceFrame.create_hybrid
        self.surface_vel_RF = self.create_hybrid(
            position=self.orbital_RF, rotation=self.surface_RF)

        # in-game time
        self.ut = self.stream(getattr, self.KSC, 'ut')
        self.met = self.stream(getattr, self.vessel, 'met')

        # position
        self.position = self.stream(
            self.vessel.position, self.orbit.body.reference_frame)

        # vessel
        self.mass = self.stream(getattr, self.vessel, 'mass')
        self.dry_mass = self.stream(getattr, self.vessel, 'dry_mass')
        self.crew_capacity = self.stream(getattr, self.vessel, 'crew_capacity')
        self.crew_count = self.stream(getattr, self.vessel, 'crew_count')
        self.crew = self.stream(getattr, self.vessel, 'crew')
        self.current_biome = self.stream(getattr, self.vessel, 'biome')

        # resources
        SF_amt = self.call(self.fuel_amount, 'SolidFuel')
        LF_amt = self.call(self.fuel_amount, 'LiquidFuel')
        OX_amt = self.call(self.fuel_amount, 'Oxidizer')
        MP_amt = self.call(self.fuel_amount, 'MonoPropellant')

        # vessel engines
        self.engine = self.vessel.parts.engines[0]
        self.engine_is_active = self.stream(getattr, self.engine, 'active')
        self.thrust = self.stream(getattr, self.engine, 'thrust')
        self.available_thrust = self.stream(
            getattr, self.engine, 'available_thrust')
        self.max_thrust_asl = self.stream(getattr, self.engine, 'max_thrust')
        self.max_thrust_vac = self.stream(
            getattr, self.engine, 'max_vacuum_thrust')
        self.Isp_asl = self.stream(
            getattr, self.engine, 'kerbin_sea_level_specific_impulse')
        self.Isp = self.stream(getattr, self.engine, 'specific_impulse')
        self.Isp_vac = self.stream(
            getattr, self.engine, 'vacuum_specific_impulse')
        self.fuel_types = self.stream(getattr, self.engine, 'propellant_names')
        self.fuel_ratio = self.stream(
            getattr, self.engine, 'propellant_ratios')
        self.got_fuel = self.stream(getattr, self.engine, 'has_fuel')
        self.throttle = self.stream(getattr, self.engine, 'throttle')

        # surface data
        self.current_biome = self.stream(getattr, self.vessel, 'biome')

        # surface flight
        self.altitude = self.stream(
            getattr, self.flight(self.surface_RF), 'mean_altitude')
        self.surface_speed = self.stream(
            getattr, self.flight(self.surface_RF), 'speed')
        self.surface_vel = self.stream(
            getattr, self.flight(self.surface_vel_RF), 'velocity')
        self.vert_speed = self.stream(
            getattr, self.flight(self.surface_RF), 'vertical_speed')
        self.slip_angle = self.stream(
            getattr, self.flight(self.surface_RF), 'sideslip_angle')
        self.static_temp = self.stream(getattr, self.flight(
            self.surface_RF), 'static_air_temperature')
        self.pitch = self.stream(
            getattr, self.flight(self.surface_RF), 'pitch')
        self.heading = self.stream(
            getattr, self.flight(self.surface_RF), 'heading')
        self.roll = self.stream(getattr, self.flight(self.surface_RF), 'roll')
        self.aoa = self.stream(getattr, self.flight(
            self.surface_RF), 'angle_of_attack')
        self.p_atmo = self.stream(getattr, self.flight(
            self.surface_RF), 'atmosphere_density')
        self.q = self.stream(getattr, self.flight(
            self.surface_RF), 'dynamic_pressure')
        self.g_force = self.stream(
            getattr, self.flight(self.surface_RF), 'g_force')
        self.v_terminal = self.stream(getattr, self.flight(
            self.surface_RF), 'terminal_velocity')
        self.static_temp = self.stream(getattr, self.flight(
            self.surface_RF), 'static_air_temperature')

        # orbital flight
        self.orbital_speed = self.stream(
            getattr, self.flight(self.orbital_RF), 'speed')
        self.apoapsis = self.stream(getattr, self.orbit, 'apoapsis_altitude')
        self.time_to_apo = self.stream(getattr, self.orbit, 'time_to_apoapsis')
        self.periapsis = self.stream(getattr, self.orbit, 'periapsis_altitude')
        self.time_to_pe = self.stream(getattr, self.orbit, 'time_to_periapsis')
        self.inclination = self.stream(getattr, self.orbit, 'inclination')
        self.ecc = self.stream(getattr, self.orbit, 'eccentricity')

    def __repr__(self):
        """returns class name and instance attributes as dictionary keys"""
        return f"{self.__class__.__name__}({self.__dict__.keys()})"

    # Telemetry methods
    def get_attitude(self):
        return f"pitch,heading,roll: {self.pitch()}, {self.heading()}, {self.slip_angle()}"

    # Basic vector operations
    def V_mag(self, v):
        """returns the magnitude of a vector in 3 dimensions"""
        return math.sqrt((v[0]) ** 2 + (v[1]) ** 2 + (v[2]) ** 2)

    def dot_p(self, u, v):
        """ method 1 for dot product calculation to find angle  """
        return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]

    def cross_p(self, u, v):
        """ returns the cross product of two vectors u x v - orthogonal to u and v """
        return (u[1]*v[2] - u[2]*v[1],
                u[2]*v[0] - u[0]*v[2],
                u[0]*v[1] - u[1]*v[0])

    def UV_theta(self, u, v):
        """ returns angle between vectors, checks if they are parallel """
        dotp = dot_p(u, v)
        if dotp == 0:
            return 0
        else:
            theta = math.acos(dotp / (V_mag(u) * V_mag(v))) * (180/math.pi)
            return theta
