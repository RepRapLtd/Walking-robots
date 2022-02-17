EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Diode_Bridge:DF06M D1
U 1 1 620CD66E
P 4325 3575
F 0 "D1" H 4669 3621 50  0000 L CNN
F 1 "DF06M" H 4669 3530 50  0000 L CNN
F 2 "Diode_THT:Diode_Bridge_DIP-4_W7.62mm_P5.08mm" H 4475 3700 50  0001 L CNN
F 3 "http://www.vishay.com/docs/88571/dfm.pdf" H 4325 3575 50  0001 C CNN
	1    4325 3575
	1    0    0    -1  
$EndComp
$Comp
L Diode_Bridge:DF06M D2
U 1 1 620CDFE9
P 4325 4450
F 0 "D2" H 4669 4496 50  0000 L CNN
F 1 "DF06M" H 4669 4405 50  0000 L CNN
F 2 "Diode_THT:Diode_Bridge_DIP-4_W7.62mm_P5.08mm" H 4475 4575 50  0001 L CNN
F 3 "http://www.vishay.com/docs/88571/dfm.pdf" H 4325 4450 50  0001 C CNN
	1    4325 4450
	1    0    0    -1  
$EndComp
Wire Wire Line
	4025 3575 3875 3575
Wire Wire Line
	3875 3575 3875 4000
Wire Wire Line
	3875 4450 4025 4450
Wire Wire Line
	4625 3575 4725 3575
Wire Wire Line
	4725 3575 4725 3900
Wire Wire Line
	4725 4450 4625 4450
$Comp
L Connector:Conn_01x04_Male J1
U 1 1 620D0CE0
P 3400 3975
F 0 "J1" H 3508 4256 50  0000 C CNN
F 1 "Conn_01x04_Male" H 3508 4165 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" H 3400 3975 50  0001 C CNN
F 3 "~" H 3400 3975 50  0001 C CNN
	1    3400 3975
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Male J2
U 1 1 620D1337
P 5475 4000
F 0 "J2" H 5447 3882 50  0000 R CNN
F 1 "Conn_01x02_Male" H 5447 3973 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 5475 4000 50  0001 C CNN
F 3 "~" H 5475 4000 50  0001 C CNN
	1    5475 4000
	-1   0    0    1   
$EndComp
Wire Wire Line
	5275 3900 4725 3900
Connection ~ 4725 3900
Wire Wire Line
	4725 3900 4725 4450
Wire Wire Line
	5275 4000 3875 4000
Connection ~ 3875 4000
Wire Wire Line
	3875 4000 3875 4450
Wire Wire Line
	3600 4175 3675 4175
Wire Wire Line
	3675 4175 3675 4750
Wire Wire Line
	3675 4750 4325 4750
Wire Wire Line
	3600 4075 4325 4075
Wire Wire Line
	4325 4075 4325 4150
Wire Wire Line
	3600 3975 3750 3975
Wire Wire Line
	3750 3975 3750 3875
Wire Wire Line
	3750 3875 4325 3875
Wire Wire Line
	3600 3875 3700 3875
Wire Wire Line
	3700 3875 3700 3275
Wire Wire Line
	3700 3275 4325 3275
$Comp
L Mechanical:MountingHole H1
U 1 1 620CDEDB
P 3575 5075
F 0 "H1" H 3675 5121 50  0000 L CNN
F 1 "MountingHole" H 3675 5030 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.5mm" H 3575 5075 50  0001 C CNN
F 3 "~" H 3575 5075 50  0001 C CNN
	1    3575 5075
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H2
U 1 1 620CE4D0
P 3575 5275
F 0 "H2" H 3675 5321 50  0000 L CNN
F 1 "MountingHole" H 3675 5230 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.5mm" H 3575 5275 50  0001 C CNN
F 3 "~" H 3575 5275 50  0001 C CNN
	1    3575 5275
	1    0    0    -1  
$EndComp
$EndSCHEMATC
