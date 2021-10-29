import os
import csv


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

    i = 0
    while len(x_array) - 1 >= i:
        if i-2*imu_step >= 0:
            ax = get_acc(x_array[i], x_array[i-imu_step], x_array[i-2*imu_step], f_dt)
            ay = get_acc(y_array[i], y_array[i-imu_step], y_array[i-2*imu_step], f_dt)
            az = get_acc(z_array[i], z_array[i-imu_step], z_array[i-2*imu_step], f_dt)
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


def get_csv_data(csv_file):
    """
    param: csv_file path
    brief: reads the csv file
    return: x, y, z, roll, pitch, yaw
    """
    col1 = []
    col2 = []
    col3 = []
    col4 = []
    col5 = []
    col6 = []

    file = open(csv_file)
    csv_reader = csv.reader(file)
    header = []
    header = next(csv_reader)
    print(header)

    for row in csv_reader:
        col1.append(float(row[0]))
        col2.append(float(row[1]))
        col3.append(float(row[2]))
        col4.append(float(row[3]))
        col5.append(float(row[4]))
        col6.append(float(row[5]))

    return col1, col2, col3, col4, col5, col6


def set_csv_data(csv_file, fields, rows):

    with open(csv_file, 'w', newline='') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # # writing the data rows
        csvwriter.writerows(rows)


def write_in_csv(linear_acc, angular_vel, output_dir):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    acc_fields = ["accel_x (m/s^2)", "accel_y (m/s^2)", "accel_z (m/s^2)"]
    gyro_fields = ["gyro_x (deg/s)", "gyro_y (deg/s)", "gyro_z (deg/s)"]

    ax, ay, az = linear_acc[0], linear_acc[1], linear_acc[2]
    wx, wy, wz = angular_vel[0], angular_vel[1], angular_vel[2]

    acc_rows = []
    gyro_rows = []

    accel_file = "accel_real.csv"
    gyro_file = "gyro_real.csv"

    for idx, _ in enumerate(ax):
        acc_row = [ax[idx], ay[idx], az[idx]]
        acc_rows.append(acc_row)
        gyro_row = [wx[idx], wy[idx], wz[idx]]
        gyro_rows.append(gyro_row)

    set_csv_data(os.path.join(output_dir, accel_file), acc_fields, acc_rows)
    set_csv_data(os.path.join(output_dir, gyro_file), gyro_fields, gyro_rows)


if __name__ == "__main__":

    input_file = "../data/imu_data/imu_data_test_1.csv"
    output_dir = "../data/imu_sim_data/"

    x, y, z, roll, pitch, yaw = get_csv_data(input_file)

    ax, ay, az = cal_linear_acc(x, y, z, 24, 24)
    wx, wy, wz = cal_angular_vel(roll, pitch, yaw, 24, 24)

    linear_acc = [ax, ay, az]
    angular_vel = [wx, wy, wz]

    write_in_csv(linear_acc, angular_vel, output_dir)

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
