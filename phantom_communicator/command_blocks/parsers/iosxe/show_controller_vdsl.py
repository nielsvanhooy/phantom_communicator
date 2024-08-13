import re
from typing import Any

from phantom_communicator.command_blocks import constants as commands
from phantom_communicator.command_blocks.decorators import command_or_parse


@command_or_parse(name=commands.SHOW_CONTROLLER_VDSL, vendor=commands.CISCO, os="iosxe", type="parse_command")
def parse_show_controller_vdsl(command_results) -> dict[str, Any]:
    data = command_results.result

    ctrl_dict = {}

    # Controller VDSL 0/2/0 is UP
    p1 = re.compile(r"^[Cc]on\w+\s(?P<ctrl>\w+\s\S+)\s+\w+\s+(?P<state>\w+)$")

    # Daemon Status: UP
    p2 = re.compile(r"^(?P<param>Dae\w+\s+\w+):\s+(?P<vl>\w+)$")

    # Serial Number Near: FGL223491WW C1127X-8 17.7.20210
    # Modem Version Near: 17.7.2021 0524: 03251
    p2_1 = re.compile(r"^(?P<param>Serial\s+Number\s+Near):\s+(?P<vl>.+)$")

    # Modem Version Near: 17.7.20210524: 03251
    # Modem Version Far: 0x544d
    p2_2 = re.compile(r"^(?P<param>Modem\s+Version\s+Far):\s+(?P<vl>.+)$")

    # Modem Status: TC Sync(Showtime!)
    p2_3 = re.compile(r"^(?P<param>Modem\s+Status):\s+(?P<vl>.+)$")

    # DSL Config Mode: ADSL2 +
    p2_4 = re.compile(r"^(?P<param>DSL\s+\w+\s+\w+):\s+(?P<vl>.+)$")

    # Trained Mode: G.992.5 (ADSL2 +) Annex A
    p2_5 = re.compile(r"^(?P<param>Tr\w+\s+\w+):\s+(?P<vl>.+)$")

    # TC Mode: ATM
    p2_6 = re.compile(r"^(?P<param>TC\s+\w+):\s+(?P<vl>.+)$")

    # Selftest Result: 0x00
    p2_7 = re.compile(r"^(?P<param>Se\w+\s+\w+):\s+(?P<vl>.+)$")

    # Short inits: 0
    p2_8 = re.compile(r"^(?P<param>Sh\w+\s+\w+):\s+(?P<vl>.+)$")

    # DELT configuration: disabled
    # DELT state: not running
    p2_9 = re.compile(r"^(?P<param>DELT\s+\w+):\s+(?P<vl>.+)$")

    # Failed full inits: 0
    # Failed short inits: 0
    p2_10 = re.compile(r"^(?P<param>Failed\s+\w+\s+\w+):\s+(?P<vl>.+)$")

    # Modem FW Version: 4.14L.04
    p2_11 = re.compile(r"^(?P<param>Modem\s+FW+\s+\w+):\s+(?P<vl>.+)$")

    # Modem PHY Version: A2pv6F039x8.d26d
    # Modem PHY Source: System
    p2_12 = re.compile(r"^(?P<param>Modem\s+PHY+\s+\w+):\s+(?P<vl>.+)$")

    # SRA count: 0    0
    # Total FECC: 799014    23383
    # Total ES: 0       2
    # Total SES: 0      0
    # Total LOSS: 0     0
    # Total UAS: 46     46
    # Total LPRS: 0     0
    # Total LOFS: 0     0
    # Total LOLS: 0     0
    p3 = re.compile(r"^(?P<param>\w+\s+\w+):\s+(?P<xtr>\d+)\s+(?P<xtc>\d+)$")

    # Bit swap: enabled     enabled
    p3_1 = re.compile(r"^(?P<param>\w+\s+\w+):\s+(?P<xtr>[enabled|disable]+)\s+(?P<xtc>\w+)$")

    # Bit swap count: 18    3
    p3_2 = re.compile(r"^(?P<param>\w+\s+\w+\s+\w+):\s+(?P<xtr>\d+)\s+(?P<xtc>\d+)$")

    # Line Attenuation: 4.0 dB      2.2 dB
    # Signal Attenuation: 2.9 dB     0.0 dB
    # Noise Margin: 9.4 dB    5.8 dB
    p3_3 = re.compile(r"^(?P<param>\w+\s+\w+):\s+(?P<xtr>\d+.\d\s+dB)\s+(?P<xtc>\d+.\d\s+dB)$")

    # Actual Power: 19.1 dBm     12.1 dBm
    p3_4 = re.compile(r"^(?P<param>\w+\s+\w+):\s+(?P<xtr>\d+.\d\s+dBm)\s+(?P<xtc>.+)$")

    # Trellis: ON     ON
    # SRA: enabled    enabled
    p3_5 = re.compile(r"^(?P<param>\w+):\s+(?P<xtr>\w+)\s+(?P<xtc>\w+)$")

    # Attainable Rate: 23708 kbits/s       1351 kbits/s
    p3_6 = re.compile(r"^(?P<param>\w+\s+\w+):\s+(?P<xtr>\d+\s+\S+)\s+(?P<xtc>\d+\s+\S+)$")

    # Chip Vendor ID: 'BDCM'                   'BDCM'
    # Chip Vendor Specific: 0x0000        0x544D
    # Chip Vendor Country: 0xB500         0xB500
    # Modem Vendor ID: 'CSCO'                   'BDCM'
    # Modem Vendor Specific: 0x4602       0x544D
    # Modem Vendor Country: 0xB500        0xB500
    # Serial Number Near: FGL223491WW C1127X - 8 17.7.20210
    p3_7 = re.compile(r"^(?P<param>\w+\s+\w+\s+\w+):\s+(?P<xtr>\S+)\s+(?P<xtc>\S+.+)$")

    # Per Band Status: D1  D2  D3  U0  U1  U2  U3
    # Line Attenuation(dB): 0.9    2.4 2.4 N / A   2.0 1.1 N / A
    # Signal  Attenuation(dB): 0.9    2.4 2.4  N / A   1.5 0.6 N / A
    # Noise Margin(dB): 19.1    18.6    18.6    N / A   5.7 5.6 N / A
    p4 = re.compile(
        r"^(?P<param>\w+\s+\w+\(dB\)):\s+(?P<d1>\d+.\d+)\s+(?P<d2>\d+.\d+)\s+(?P<d3>\d+.\d+)\s+\S+\s+(?P<u1>\d+.\d+)\s+(?P<u2>\d+.\d+)\s+(?P<u3>\S+)$"
    )

    # Training Log: Stopped
    p5 = re.compile(r"^(?P<param>\w+\s+\w+)\s+:\s+(?P<state>\S+)$")

    # Training Log Filename: flash:vdsllog.bin
    p6 = re.compile(r"^(?P<param>\w+\s+\w+\s+\w+)\s+:\s+(?P<state>\S+)$")

    # DS Channel1    DS Channel0    US Channel1    US Channel0
    # Previous Speed: NA   0   NA  0
    # Total Cells: NA   145385538   NA  7799369
    # User Cells: NA   8598306 NA  447068
    # CRC Errors: NA  0   NA  3
    # Header Errors: NA  0   NA  1
    # Actual INP: NA 0.00    NA  0.00
    p7 = re.compile(
        r"^(?P<param>\w+\s\w+):\s+(?P<d_ch1>[\w\d.]+)\s+(?P<d_ch0>[\d.]+)\s+(?P<u_ch1>[\w\d.]+)\s+(?P<u_ch0>[\d.]+)$"
    )

    # Speed (kbps): NA 23756   NA  1283
    # Interleave (ms): NA  0.08    NA  0.49
    p7_1 = re.compile(
        r"^(?P<param>\w+\s\(\w+\)):\s+(?P<d_ch1>[\w\d.]+)\s+(?P<d_ch0>[\d.]+)\s+(?P<u_ch1>[\w\d.]+)\s+(?P<u_ch0>[\d.]+)$"
    )

    # SRA Previous Speed: NA   0   NA  0
    p7_2 = re.compile(
        r"^(?P<param>\w+\s\w+\s+\w+):\s+(?P<d_ch1>[\w\d.]+)\s+(?P<d_ch0>[\d.]+)\s+(?P<u_ch1>[\w\d.]+)\s+(?P<u_ch0>[\d.]+)$"
    )

    # Reed - Solomon EC: NA  0   NA  0
    p7_3 = re.compile(
        r"^(?P<param>\w+-\w+\s+\w+):\s+(?P<d_ch1>[\w\d.]+)\s+(?P<d_ch0>[\d.]+)\s+(?P<u_ch1>[\w\d.]+)\s+(?P<u_ch0>[\d.]+)$"
    )

    for lines in data.splitlines():
        line = lines.strip()

        # Controller VDSL 0/2/0 is UP
        m = p1.match(line)
        if m:
            group = m.groupdict()
            ctrl_dict["controller_vdsl"] = group["state"]

        # Daemon Status: UP
        m = p2.match(line)
        if m:
            group = m.groupdict()
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict[param] = group["vl"]

        # Serial Number Near: FGL223491WW C1127X-8 17.7.20210
        # Modem Version Near: 17.7.2021 0524: 03251\

        m = p2_1.match(line)
        if m:
            group = m.groupdict()
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict[param] = group["vl"]

        m = p2_2.match(line)
        if m:
            group = m.groupdict()
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict[param] = group["vl"]

        # Modem Status: TC Sync(Showtime!)
        m = p2_3.match(line)
        if m:
            group = m.groupdict()
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict[param] = group["vl"]

        # DSL Config Mode: ADSL2 +
        m = p2_4.match(line)
        if m:
            group = m.groupdict()
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict[param] = group["vl"]

        # Trained Mode: G.992.5 (ADSL2 +) Annex A
        m = p2_5.match(line)
        if m:
            group = m.groupdict()
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict[param] = group["vl"]

        # TC Mode: ATM
        m = p2_6.match(line)
        if m:
            group = m.groupdict()
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict[param] = group["vl"]

        # Selftest Result: 0x00
        m = p2_7.match(line)
        if m:
            group = m.groupdict()
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict[param] = group["vl"]

        # Short inits: 0
        m = p2_8.match(line)
        if m:
            group = m.groupdict()
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict[param] = int(group["vl"])

        # DELT configuration: disabled
        # DELT state: not running
        m = p2_9.match(line)
        if m:
            group = m.groupdict()
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict[param] = group["vl"]

        # Failed full inits: 0
        # Failed short inits: 0
        m = p2_10.match(line)
        if m:
            group = m.groupdict()
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict[param] = int(group["vl"])

        # Modem FW Version: 4.14L.04
        m = p2_11.match(line)
        if m:
            group = m.groupdict()
            param = re.sub(" +", " ", group["param"].lower()).replace(" ", "_")
            ctrl_dict[param] = group["vl"]

        # Modem PHY Version: A2pv6F039x8.d26d
        # Modem PHY Source: System
        m = p2_12.match(line)
        if m:
            group = m.groupdict()
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict[param] = group["vl"]

        # SRA count: 0    0
        # Total FECC: 799014    23383
        # Total ES: 0       2
        # Total SES: 0      0
        # Total LOSS: 0     0
        # Total UAS: 46     46
        # Total LPRS: 0     0
        # Total LOFS: 0     0
        # Total LOLS: 0     0
        m = p3.match(line)
        if m:
            group = m.groupdict()
            ctrl_dict.setdefault("xtu_r_ds", {})
            ctrl_dict.setdefault("xtu_c_us", {})
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict["xtu_r_ds"][param] = int(group["xtr"])
            ctrl_dict["xtu_c_us"][param] = int(group["xtc"])

        # Bit swap: enabled     enabled
        m = p3_1.match(line)
        if m:
            group = m.groupdict()
            ctrl_dict.setdefault("xtu_r_ds", {})
            ctrl_dict.setdefault("xtu_c_us", {})
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict["xtu_r_ds"][param] = group["xtr"]
            ctrl_dict["xtu_c_us"][param] = group["xtc"]

        # Bit swap count: 18    3
        m = p3_2.match(line)
        if m:
            group = m.groupdict()
            ctrl_dict.setdefault("xtu_r_ds", {})
            ctrl_dict.setdefault("xtu_c_us", {})
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict["xtu_r_ds"][param] = group["xtr"]
            ctrl_dict["xtu_c_us"][param] = group["xtc"]

        # Line Attenuation: 4.0 dB      2.2 dB
        # Signal Attenuation: 2.9 dB     0.0 dB
        # Noise Margin: 9.4 dB    5.8 dB
        m = p3_3.match(line)
        if m:
            group = m.groupdict()
            ctrl_dict.setdefault("xtu_r_ds", {})
            ctrl_dict.setdefault("xtu_c_us", {})
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict["xtu_r_ds"][param] = group["xtr"]
            ctrl_dict["xtu_c_us"][param] = group["xtc"]

        # Actual Power: 19.1 dBm     12.1 dBm
        m = p3_4.match(line)
        if m:
            group = m.groupdict()
            ctrl_dict.setdefault("xtu_r_ds", {})
            ctrl_dict.setdefault("xtu_c_us", {})
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict["xtu_r_ds"][param] = group["xtr"]
            ctrl_dict["xtu_c_us"][param] = group["xtc"]

        # Trellis: ON     ON
        # SRA: enabled    enabled
        m = p3_5.match(line)
        if m:
            group = m.groupdict()
            ctrl_dict.setdefault("xtu_r_ds", {})
            ctrl_dict.setdefault("xtu_c_us", {})
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict["xtu_r_ds"][param] = group["xtr"]
            ctrl_dict["xtu_c_us"][param] = group["xtc"]

        # Attainable Rate: 23708 kbits/s       1351 kbits/s
        m = p3_6.match(line)
        if m:
            group = m.groupdict()
            ctrl_dict.setdefault("xtu_r_ds", {})
            ctrl_dict.setdefault("xtu_c_us", {})
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict["xtu_r_ds"][param] = group["xtr"]
            ctrl_dict["xtu_c_us"][param] = group["xtc"]

        # Chip Vendor ID: 'BDCM'                   'BDCM'
        # Chip Vendor Specific: 0x0000        0x544D
        # Chip Vendor Country: 0xB500         0xB500
        # Modem Vendor ID: 'CSCO'                   'BDCM'
        # Modem Vendor Specific: 0x4602       0x544D
        # Modem Vendor Country: 0xB500        0xB500
        # Serial Number Near: FGL223491WW C1127X - 8 17.7.20210
        m = p3_7.match(line)
        if m:
            group = m.groupdict()
            ctrl_dict.setdefault("xtu_r_ds", {})
            ctrl_dict.setdefault("xtu_c_us", {})
            param = m.groupdict()["param"]
            # xtr_val = m.groupdict()["xtr"]
            # xtc_val = m.groupdict()["xtc"]
            param_v = group["param"]
            param = group["param"].lower().replace(" ", "_")
            if param_v == "Per Band Status":
                continue
            elif param_v == "SRA Previous Speed":
                continue
            elif param_v == "Serial Number Near":
                continue
            elif "chip" in param:
                ctrl_dict["xtu_r_ds"].setdefault("chip_vendor", {})
                ctrl_dict["xtu_c_us"].setdefault("chip_vendor", {})
                ctrl_dict["xtu_r_ds"]["chip_vendor"][param] = group["xtr"]
                ctrl_dict["xtu_c_us"]["chip_vendor"][param] = group["xtc"]
            elif "modem" in param:
                ctrl_dict["xtu_r_ds"].setdefault("modem_vendor", {})
                ctrl_dict["xtu_c_us"].setdefault("modem_vendor", {})
                ctrl_dict["xtu_r_ds"]["modem_vendor"][param] = group["xtr"]
                ctrl_dict["xtu_c_us"]["modem_vendor"][param] = group["xtc"]
            else:
                ctrl_dict["xtu_r_ds"][param] = group["xtr"]
                ctrl_dict["xtu_c_us"][param] = group["xtc"]

        # Per Band Status: D1  D2  D3  U0  U1  U2  U3
        # Line Attenuation(dB): 0.9    2.4 2.4 N / A   2.0 1.1 N / A
        # Signal  Attenuation(dB): 0.9    2.4 2.4  N / A   1.5 0.6 N / A
        # Noise Margin(dB): 19.1    18.6    18.6    N / A   5.7 5.6 N / A
        m = p4.match(line)
        if m:
            group = m.groupdict()
            ctrl_dict.setdefault("xtu_r_ds", {})
            ctrl_dict.setdefault("xtu_c_us", {})
            ctrl_dict["xtu_r_ds"].setdefault("d1", {})
            ctrl_dict["xtu_r_ds"].setdefault("d2", {})
            ctrl_dict["xtu_r_ds"].setdefault("d3", {})
            ctrl_dict["xtu_c_us"].setdefault("u1", {})
            ctrl_dict["xtu_c_us"].setdefault("u2", {})
            ctrl_dict["xtu_c_us"].setdefault("u3", {})
            par = group["param"].lower().replace(" ", "_")
            ctrl_dict["xtu_r_ds"]["d1"][par] = group["d1"]
            ctrl_dict["xtu_r_ds"]["d2"][par] = group["d2"]
            ctrl_dict["xtu_r_ds"]["d3"][par] = group["d3"]
            ctrl_dict["xtu_c_us"]["u1"][par] = group["u1"]
            ctrl_dict["xtu_c_us"]["u2"][par] = group["u2"]
            ctrl_dict["xtu_c_us"]["u3"][par] = group["u3"]

        # Training Log: Stopped
        m = p5.match(line)
        if m:
            group = m.groupdict()
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict[param] = group["state"]

        # Training Log Filename: flash:vdsllog.bin
        m = p6.match(line)
        if m:
            group = m.groupdict()
            param.lower().replace(" ", "_")
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict[param] = group["state"]

        # DS Channel1    DS Channel0    US Channel1    US Channel0
        # Previous Speed: NA   0   NA  0
        # Total Cells: NA   145385538   NA  7799369
        # User Cells: NA   8598306 NA  447068
        # CRC Errors: NA  0   NA  3
        # Header Errors: NA  0   NA  1
        # Actual INP: NA 0.00    NA  0.00
        m = p7.match(line)
        if m:
            group = m.groupdict()
            ctrl_dict.setdefault("xtu_r_ds", {})
            ctrl_dict.setdefault("xtu_c_us", {})
            ctrl_dict["xtu_r_ds"].setdefault("ds_channel1", {})
            ctrl_dict["xtu_r_ds"].setdefault("ds_channel0", {})
            ctrl_dict["xtu_c_us"].setdefault("us_channel1", {})
            ctrl_dict["xtu_c_us"].setdefault("us_channel0", {})
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict["xtu_r_ds"]["ds_channel1"][param] = group["d_ch1"]
            ctrl_dict["xtu_r_ds"]["ds_channel0"][param] = group["d_ch0"]
            ctrl_dict["xtu_c_us"]["us_channel1"][param] = group["u_ch1"]
            ctrl_dict["xtu_c_us"]["us_channel0"][param] = group["u_ch0"]

        # Speed (kbps): NA 23756   NA  1283
        # Interleave (ms): NA  0.08    NA  0.49
        m = p7_1.match(line)
        if m:
            group = m.groupdict()
            ctrl_dict.setdefault("xtu_r_ds", {})
            ctrl_dict.setdefault("xtu_c_us", {})
            ctrl_dict["xtu_r_ds"].setdefault("ds_channel1", {})
            ctrl_dict["xtu_r_ds"].setdefault("ds_channel0", {})
            ctrl_dict["xtu_c_us"].setdefault("us_channel1", {})
            ctrl_dict["xtu_c_us"].setdefault("us_channel0", {})
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict["xtu_r_ds"]["ds_channel1"][param] = group["d_ch1"]
            ctrl_dict["xtu_r_ds"]["ds_channel0"][param] = group["d_ch0"]
            ctrl_dict["xtu_c_us"]["us_channel1"][param] = group["u_ch1"]
            ctrl_dict["xtu_c_us"]["us_channel0"][param] = group["u_ch0"]

        # SRA Previous Speed: NA   0   NA  0
        m = p7_2.match(line)
        if m:
            group = m.groupdict()
            ctrl_dict.setdefault("xtu_r_ds", {})
            ctrl_dict.setdefault("xtu_c_us", {})
            ctrl_dict["xtu_r_ds"].setdefault("ds_channel1", {})
            ctrl_dict["xtu_r_ds"].setdefault("ds_channel0", {})
            ctrl_dict["xtu_c_us"].setdefault("us_channel1", {})
            ctrl_dict["xtu_c_us"].setdefault("us_channel0", {})
            param = group["param"].lower().replace(" ", "_")
            ctrl_dict["xtu_r_ds"]["ds_channel1"][param] = group["d_ch1"]
            ctrl_dict["xtu_r_ds"]["ds_channel0"][param] = group["d_ch0"]
            ctrl_dict["xtu_c_us"]["us_channel1"][param] = group["u_ch1"]
            ctrl_dict["xtu_c_us"]["us_channel0"][param] = group["u_ch0"]

        # Reed - Solomon EC: NA  0   NA  0
        m = p7_3.match(line)
        if m:
            group = m.groupdict()
            ctrl_dict.setdefault("xtu_r_ds", {})
            ctrl_dict.setdefault("xtu_c_us", {})
            ctrl_dict["xtu_r_ds"].setdefault("ds_channel1", {})
            ctrl_dict["xtu_r_ds"].setdefault("ds_channel0", {})
            ctrl_dict["xtu_c_us"].setdefault("us_channel1", {})
            ctrl_dict["xtu_c_us"].setdefault("us_channel0", {})
            param_1 = group["param"].lower().replace(" ", "_")
            param = param_1.replace("-", "_")
            ctrl_dict["xtu_r_ds"]["ds_channel1"][param] = group["d_ch1"]
            ctrl_dict["xtu_r_ds"]["ds_channel0"][param] = group["d_ch0"]
            ctrl_dict["xtu_c_us"]["us_channel1"][param] = group["u_ch1"]
            ctrl_dict["xtu_c_us"]["us_channel0"][param] = group["u_ch0"]

    return ctrl_dict
