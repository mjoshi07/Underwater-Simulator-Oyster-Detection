def get_vel(p2, p1, dt):
    v = (p2 - p1)/dt
    return v


def get_acc(p3, p2, p1, dt):
    v1 = get_vel(p2, p1, dt)
    v2 = get_vel(p3, p2, dt)

    a = (v2 - v1)/dt
    return a


def cal_imu_step(imu_rate, frame_rate):
    """
    f_dt = 1.0/frame_rate
    imu_dt = 1.0/imu_rate

    1 imu_step correspond to f_dt, i.e after reading ith value from position array, read the (i+imu_step) indexed value
    """

    imu_step = int(imu_rate/frame_rate)  # (f_dt/imu_dt)

    return imu_step


def cal_linear_acc(x_array, y_array, z_array, imu_rate=30.0, frame_rate=30.0):
    """
    param: array of positions for x, y, z
    brief: at least 3 positions values for x y z each from time t1 to t2 to t3 or tn
            we will be calculating the values at frame_rate of video, i.e at 30 frame_rate if not specified
    return: ax, ay, az
    """
    ax_array = []
    ay_array = []
    az_array = []

    f_dt = 1.0/frame_rate

    imu_step = cal_imu_step(imu_rate, frame_rate)

    gravity_in_z = -9.8  # meters/second squared

    i = 0
    while len(x_array) - 1 >= i:
        if i-2*imu_step >= 0:
            ax = get_acc(x_array[i], x_array[i-imu_step], x_array[i-2*imu_step], f_dt)
            ay = get_acc(y_array[i], y_array[i-imu_step], y_array[i-2*imu_step], f_dt)
            az = get_acc(z_array[i], y_array[i-imu_step], z_array[i-2*imu_step], f_dt) + gravity_in_z

            ax_array.append(ax)
            ay_array.append(ay)
            az_array.append(az)

        i += imu_step


    return ax_array, ay_array, az_array


def cal_angular_vel(roll_array, pitch_array, yaw_array, imu_rate=30.0, frame_rate=30.0):
    """
    param: array of positions for roll, pitch, yaw
    brief: at least 2 positions values for roll pitch yaw each from time t1 to t2
    return: wx, wy, wz
    """
    wx_array = []
    wy_array = []
    wz_array = []

    f_dt = 1.0/frame_rate
    imu_step = cal_imu_step(imu_rate, frame_rate)

    i = 0
    while len(roll_array) - 1 >= i:

        if i-imu_step >= 0:
            wx = get_vel(roll_array[i], roll_array[i - imu_step], f_dt)
            wy = get_vel(pitch_array[i], pitch_array[i - imu_step], f_dt)
            wz = get_vel(yaw_array[i],  yaw_array[i - imu_step], f_dt)

            wx_array.append(wx)
            wy_array.append(wy)
            wz_array.append(wz)

        i += imu_step

    return wx_array, wy_array, wz_array


def accelerometer_demo():
    t_array = []
    x_array = []
    y_array = []
    z_array = []

    dist = 0.0
    dt = 0.0
    offset = 150  # initial position
    accel = 2  # meter/second squared
    imu_rate = 120.0
    v_rate = 30.0

    acc_is_const = True

    """
    generate some position data according to a fixed acceleration
    check whether we can get back the same value for acceleration       
    """
    for i in range(100):
        dist = offset + accel * 0.5 * (dt ** 2)
        x_array.append(dist)
        y_array.append(dist)
        z_array.append(dist)
        t_array.append(dt)
        dt += 1.0 / imu_rate

    print(t_array[:5])
    print(x_array[:5])
    print(y_array[:5])
    print(z_array[:5])
    ax, ay, az = cal_linear_acc(x_array, y_array, z_array, imu_rate, v_rate)
    print('\n')
    print(ax[:])
    print(ay[:])
    print(az[:])


def gyroscope_demo():
    t_array = []
    roll_array = []
    pitch_array = []
    yaw_array = []

    angle = 0.0
    dt = 0.0
    offset_angle = 359.5  # initial position
    angular_vel = 2  # degrees/second
    imu_rate = 120.0
    v_rate = 30.0

    """
    generate some angle data according to a fixed angular velocity
    check whether we can get back the same value for angular velocity      
    """
    for i in range(100):
        angle = offset_angle + angular_vel * dt
        roll_array.append(angle)
        pitch_array.append(angle)
        yaw_array.append(angle)
        t_array.append(dt)
        dt += 1.0 / imu_rate

    print(t_array[:5])
    print(roll_array[:5])
    print(pitch_array[:5])
    print(yaw_array[:5])
    wx, wy, wz = cal_angular_vel(roll_array, pitch_array, yaw_array, imu_rate, v_rate)
    print('\n')
    print(wx[:])
    print(wy[:])
    print(wz[:])


if __name__ == "__main__":

    """
    Generate some position data with a known acceleration value
    and then calculate acceleration from position data to verify
    """
    # accelerometer_demo()

    """
    Generate some angular data with a known angular velocity value
    and then calculate angular velocity from position data to verify
    """
    # gyroscope_demo()
