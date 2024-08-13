import re
from typing import Any, List

from phantom_communicator.command_blocks import constants as commands
from phantom_communicator.command_blocks.decorators import command_or_parse


@command_or_parse(name=commands.SHOW_RUN_INTERFACES, vendor=commands.CISCO, os="iosxe", type="parse_command")
def parse_show_run_interfaces(command_results) -> list[Any]:
    data = command_results.result

    # Init vars
    config_dict = {}

    # interface GigabitEthernet0
    p1 = re.compile(r"^interface +(?P<interface>.*?)((?=\s)|$)")

    # description "Boot lan interface"
    # description ISE Controlled Port
    p2 = re.compile(r"^description +(?P<description>[\S\s]+)$")

    # vrf forwarding Mgmt-intf
    # ip vrf forwarding oam
    p3 = re.compile(r"^(ip )?vrf +forwarding +(?P<vrf>[\S\s]+)$")

    # ip address 10.1.21.249 255.255.255.0
    p4 = re.compile(r"^ip +address +(?P<ip>[\S]+) +(?P<netmask>[\S]+)$")

    # ip address 10.1.21.249 255.255.255.0 secondary
    p4_1 = re.compile(r"^ip +address +(?P<ip>[\S]+) +(?P<netmask>[\S]+)\s(?P<secondary>secondary)$")

    # ipv6 address 2001:db8:4:1::1/64
    # ipv6 address 2001:db8:400:1::2/112
    p5 = re.compile(r"^ipv6 address +(?P<ipv6>.+)$")

    # shutdown
    p6 = re.compile(r"^(?P<shutdown>shutdown)$")

    # encapsulation dot1Q 201
    p7 = re.compile(r"^encapsulation +dot1(q|Q) +(?P<dot1q>([\d]+|[\d\-,]+))$")

    # encapsulation ppp
    p7_1 = re.compile(r"^encapsulation ppp$")

    # carrier-delay up 60
    # carrier-delay down 60
    p8 = re.compile(r"^carrier-delay +(?P<carrier_delay>.+)$")

    # negotiation auto
    # no negotiation auto
    p9 = re.compile(r"^(?P<negotiation>no +)?negotiation +auto$")

    # cdp enable
    p10 = re.compile(r"^cdp +(?P<cdp>enable)$")

    # no keepalive
    p11 = re.compile(r"^(?P<keepalive>no +)?keepalive$")

    # switchport access vlan 70
    p12 = re.compile(r"^switchport +access +vlan +(?P<vlan>[\d]+)$")

    # switchport mode access
    p13 = re.compile(r"^switchport +mode +(?P<switchport_mode>[\S\s]+)$")

    # switchport nonegotiate
    p14 = re.compile(r"^switchport +(?P<nonegotiate>nonegotiate)$")

    # ip arp inspection limit rate 1024
    p15 = re.compile(r"^ip +arp +inspection +limit +rate +(?P<rate>[\d]+)$")

    # load-interval 30
    p16 = re.compile(r"^load-interval +(?P<load_interval>\d+)$")

    # authentication control-direction in
    p17 = re.compile(r"^authentication +control-direction +(?P<direction>\w+)$")

    # authentication event fail action next-method
    p18 = re.compile(r"^authentication +event +fail +action +(?P<action>[\S\s]+)$")

    # authentication host-mode multi-auth
    p19 = re.compile(r"^authentication +host-mode +(?P<host_mode>[\S\s]+)$")

    # authentication order dot1x mab
    p20 = re.compile(r"^authentication +order +(?P<order>[\S\s]+)$")

    # authentication priority dot1x mab
    p21 = re.compile(r"^authentication +priority +(?P<priority>[\S\s]+)$")

    # authentication port-control auto
    p22 = re.compile(r"^authentication +port-control +(?P<port_control>[\S\s]+)$")

    # authentication periodic
    p23 = re.compile(r"^(?P<periodic>authentication periodic)$")

    # authentication timer reauthenticate server
    p24 = re.compile(r"^(?P<reauth>authentication +timer +reauthenticate +server)$")

    # authentication timer inactivity 65535
    p24_1 = re.compile(r"^authentication +timer +inactivity +(?P<inactivity>\d+)$")

    # authentication timer reauthenticate 6000
    p24_2 = re.compile(r"^authentication timer reauthenticate (?P<authentication_timer_reauthenticate>\d+)$")

    # authentication violation restrict
    p25 = re.compile(r"^authentication +violation +(?P<violation>[\S\s]+)$")

    # authentication fallback dot1x
    p26 = re.compile(r"^authentication +fallback +(?P<fallback>[\S\s]+)$")

    # mab
    p27 = re.compile(r"^(?P<mab>mab)$")

    # snmp trap mac-notification change added
    p28 = re.compile(r"^snmp +trap +mac-notification +change +added$")

    # snmp trap mac-notification change removed
    p29 = re.compile(r"^snmp +trap +mac-notification +change +removed$")

    # no snmp trap link-status
    p30 = re.compile(r"^no +snmp +trap +link-status$")

    # dot1x pae authenticator
    p31 = re.compile(r"^dot1x +pae +authenticator$")

    # dot1x timeout quiet-period 5
    p32 = re.compile(r"^dot1x +timeout +quiet-period +(?P<quiet_period>\d+)$")

    # dot1x timeout server-timeout 10
    p33 = re.compile(r"^dot1x +timeout +server-timeout +(?P<server_timeout>\d+)$")

    # dot1x timeout tx-period 5
    p34 = re.compile(r"^dot1x +timeout +tx-period +(?P<tx_period>\d+)$")

    # spanning-tree portfast
    p35 = re.compile(r"^spanning-tree +portfast$")

    # spanning-tree bpduguard enable
    p36 = re.compile(r"^spanning-tree +bpduguard +(?P<bpduguard>[\S\s]+)$")

    # ip dhcp snooping limit rate 100
    p37 = re.compile(r"^ip +dhcp +snooping +limit +rate +(?P<rate>[\d]+)$")

    # ipv6 enable
    p38 = re.compile(r"^ipv6 enable$")

    # ip ospf 2 area 0
    # ipv6 ospf 1 area 0
    p39 = re.compile(r"^(?P<ip>ip|ipv6) +ospf +(?P<ospf>\d+) +area +(?P<area>[\d]+)$")

    # ospfv3 1 ipv6 area 0
    p40 = re.compile(r"^ospfv3 +(?P<rate>[\d]+) +ipv6 +area +(?P<area>[\d]+)$")

    # channel-group 1 mode active
    p41 = re.compile(r"^channel-group +(?P<group>[\d]+) +mode +(?P<mode>[\w]+)$")

    # power inline port priority high
    p42 = re.compile(r"^power +inline +port +priority +(?P<power_priority>[\w]+)$")

    # power inline static max 20000
    p43 = re.compile(r"^power +inline +(?P<state>never|static)( +max +(?P<max_watts>[\d]+))?$")

    # spanning-tree bpdufilter enable
    p44 = re.compile(r"^spanning-tree +bpdufilter +(?P<bpdufilter>[\S\s]+)$")

    # ip flow monitor IPv4NETFLOW input
    p45 = re.compile(r"^ip +flow +monitor +(?P<flow_monitor_input>[\w]+) +input$")

    # switchport protected
    p46 = re.compile(r"^switchport +protected$")

    # switchport block unicast
    p47 = re.compile(r"^switchport +block +unicast$")

    # switchport block multicast
    p48 = re.compile(r"^switchport +block +multicast$")

    # switchport trunk allowed vlan 820,900-905
    # switchport trunk allowed vlan add 905-908
    p49 = re.compile(r"^switchport +trunk +allowed +vlan( +add)? (?P<vlans>[\S\s]+)$")

    # ip dhcp snooping trust
    p50 = re.compile(r"^ip +dhcp +snooping +trust$")

    # ip arp inspection trust
    p51 = re.compile(r"^ip +arp +inspection +trust$")

    # ip unnumbered Loopback0
    p52 = re.compile(r"^ip unnumbered (?P<src_address>\S+)$")

    # tunnel mode mpls traffic-eng
    p53 = re.compile(r"^tunnel mode (?P<tunnel_mode>[a-zA-Z\- ]+)$")

    # tunnel destination 2.2.2.2
    p54 = re.compile(r"^tunnel destination (?P<tunnel_dst>\S+)$")

    # tunnel mpls traffic-eng priority 7 7
    p55 = re.compile(r"^tunnel mpls traffic-eng priority (?P<value>[a-zA-Z0-9 ]+)$")

    # tunnel mpls traffic-eng bandwidth 500
    p56 = re.compile(r"^tunnel mpls traffic-eng bandwidth (?P<value>[0-9 ]+)$")

    # tunnel mpls traffic-eng path-option 1 dynamic
    p57 = re.compile(
        r"^tunnel mpls traffic-eng path-option (?P<value>[0-9]+)\s*(?:explicit name)? +(?P<path_type>\S+)$"
    )

    # mpls ip
    p58 = re.compile(r"^mpls ip$")

    # service-policy input AutoQos-4.0-CiscoPhone-Input-Policy
    p59 = re.compile(r"^service-policy\s+(in|input)\s+(?P<input_policy>\S+)$")

    # service-policy output AutoQos-4.0-Output-Policy
    p60 = re.compile(r"^service-policy\s+(out|output)\s+(?P<output_policy>\S+)$")

    # switchport port-security mac-address sticky 1020.4bb1.6f2f
    p61 = re.compile(r"^switchport port-security mac-address sticky (?P<value>([a-fA-F\d]{4}\.){2}[a-fA-F\d]{4})$")

    # source template USER_NoAuth
    p62 = re.compile(r"^source template (?P<template>\w+)$")

    # host-reachability protocol bgp
    p63 = re.compile(r"^host-reachability protocol (?P<protocol>[a-zA-Z]+)$")

    # source-interface loopback1
    p64 = re.compile(r"^source-interface (?P<src_intf>[a-zA-Z0-9\-]+)$")

    # member vni 20011 ingress-replication
    p65 = re.compile(r"^member vni (?P<vni>[0-9]+) ingress-replication$")

    # member vni 20012 mcast-group 224.1.1.1
    p66 = re.compile(r"^member vni (?P<vni>[0-9]+) mcast-group (?P<ip>[0-9\.]+)$")

    # member vni 20011 ingress-replication local-routing
    p67 = re.compile(r"^member vni (?P<vni>[0-9]+) ingress-replication " r"local-routing$")

    # member vni 20011
    p68 = re.compile(r"^member vni (?P<vni>[0-9]+)$")

    # ingress-replication 1.1.1.1
    p69 = re.compile(r"^ingress-replication (?P<ip>[0-9\.]+)$")

    # member vni 20012 mcast-group 224.1.1.1 local-routing
    p70 = re.compile(r"^member vni (?P<vni>[0-9]+) mcast-group (?P<ip>[0-9\.]+) " r"local-routing$")

    # member vni 30000 vrf red
    p71 = re.compile(r"^member vni (?P<vni>[0-9]+) vrf (?P<vrf>[a-zA-Z\-]+)$")

    # ip access-group DELETE_ME in ; ip access-group TEST-OUT out
    p72 = re.compile(r"^ip access-group (?P<acl_name>[\w\-.#<>]+) (?P<direction>\w+)$")

    # lisp mobility 20_1_1_0-global-IPV4
    p73 = re.compile(r"^\s*lisp mobility +(?P<lisp_mobility>[\w-]+)$")

    # trust device cisco-phone / trust device ip-camera
    p74 = re.compile(r"^trust\sdevice\s(?P<trust_device>\S+)$")

    # ipv6 destination-guard attach-policy Univ-v6-IPDG-Policy1
    p75 = re.compile(r"^ipv6\sdestination-guard\sattach-policy\s(?P<ipv6_destination_guard_attach_policy>\S+)$")

    # ipv6 source-guard attach-policy Univ-v6-IPSG-Policy2
    p76 = re.compile(r"^ipv6\ssource-guard\sattach-policy\s(?P<ipv6_source_guard_attach_policy>\S+)$")

    # spanning-tree portfast trunk
    p77 = re.compile(r"^spanning-tree +portfast +trunk$")

    # ipv6 nd raguard attach-policy Univ_IPv6_RA_Policy_Host
    p78 = re.compile(r"^ipv6\snd\sraguard\sattach-policy\s+(?P<ipv6_nd_raguard_attach_policy>\S+)$")

    # device-tracking attach-policy IPDT_POLICY
    p79 = re.compile(r"^device-tracking\sattach-policy\s+(?P<device_tracking_attach_policy>\S+)$")

    # stackwise-virtual link 1
    p80 = re.compile(r"^stackwise-virtual\slink\s+(?P<stackwise_virtual_link>\d+)$")

    # stackwise-virtual dual-active-detection
    p81 = re.compile(r"^stackwise-virtual\s+(?P<dual_active_detection>\S+)$")

    # ip flow monitor monitor_ipv4_out output
    p82 = re.compile(r"^ip\s+flow\s+monitor\s+(?P<flow_monitor_output>\S+)\s+output$")

    # ip dhcp snooping information option allow-untrusted
    p83 = re.compile(r"^ip +dhcp +snooping +information +option +allow-untrusted$")

    # no ip dhcp snooping information option allow-untrusted
    p84 = re.compile(r"^no +ip +dhcp +snooping +information +option +allow-untrusted$")

    # ipv6 flow monitor monitor_ipv6_in sampler H_sampler input
    p85 = re.compile(r"^ipv6\s+flow\s+monitor\s+(?P<flow_monitor_input_v6>[\S]+)\s+sampler\s+[\S]+\s+input$")

    # ipv6 flow monitor monitor_ipv6_out sampler H_sampler output
    p86 = re.compile(r"^ipv6\s+flow\s+monitor\s+(?P<flow_monitor_output_v6>[\S]+)\s+sampler\s+[\S]+\s+output$")

    # speed 25000
    p87 = re.compile(r"^speed +(?P<speed>\d+)$")

    # speed nonegotiate
    p88 = re.compile(r"^speed +(?P<speed_nonegotiate>nonegotiate)$")

    # isis network point-to-point
    p89 = re.compile(r"^isis +network +(?P<isis_network>\S+)$")

    # isis metric 22 level-1
    # isis metric 22 level-2
    p90 = re.compile(r"^isis +metric +(?P<isis_v4_metric>\d+) +(?P<isis_v4_level>\S+)$")

    # isis ipv6 metric 33 level-1
    # isis ipv6 metric 22 level-2
    p91 = re.compile(r"^isis +ipv6 +metric +(?P<isis_v6_metric>\d+) +(?P<isis_v6_level>\S+)$")

    # switchport trunk native vlan 101
    p92 = re.compile(r"^switchport trunk native vlan (?P<switchport_trunk_native_vlan>\d+)$")

    # access-session host-mode multi-host
    p93 = re.compile(r"^access-session host-mode (?P<access_session_host_mode>.+)$")

    # access-session closed
    p94 = re.compile(r"^access-session (?P<access_session>\w+)$")

    # access-session port-control auto
    p95 = re.compile(r"^access-session port-control (?P<access_session_port_control>.+)$")

    # dot1x pae both
    p96 = re.compile(r"^dot1x pae (?P<dot1x_pae>.+)$")

    # dot1x timeout supp-timeout 87
    p97 = re.compile(r"^dot1x timeout supp-timeout (?P<dot1x_timeout_supp_timeout>\d+)$")

    # dot1x max-req 6
    p98 = re.compile(r"^dot1x max-req (?P<dot1x_max_req>\d+)$")

    # dot1x authenticator eap profile Self
    p99 = re.compile(r"^dot1x authenticator eap profile (?P<dot1x_authenticator_eap_profile>.+)$")

    # dot1x timeout held-period 63
    p100 = re.compile(r"^dot1x timeout held-period (?P<dot1x_timeout_held_period>\d+)$")

    # dot1x credentials EAPTLSCRED-IOSCA
    p101 = re.compile(r"^dot1x credentials (?P<dot1x_credentials>.+)$")

    # dot1x supplicant eap profile Self
    p102 = re.compile(r"^dot1x supplicant eap profile (?P<dot1x_supplicant_eap_profile>.+)$")

    # macsec
    p103 = re.compile(r"^\s*macsec$")

    # macsec access-control should-secure
    p104 = re.compile(r"^\s*macsec access-control +(?P<macsec_access_control>[\w\-]+)")

    #  mka policy MKAPolicy
    p105 = re.compile(r"^\s*mka policy +(?P<mka_policy>\S+)")

    # mka pre-shared-key key-chain KCP256
    p106 = re.compile(r"^\s*mka pre-shared-key key-chain +(?P<mka_primary_keychain>\S+)$")

    # mka pre-shared-key key-chain KCP256 fallback-key-chain KCF256
    p107 = re.compile(
        r"^\s*mka pre-shared-key key-chain +(?P<mka_primary_keychain>\S+) fallback-key-chain +(?P<mka_fallback_keychain>\S+)"
    )

    # ip mtu 1468
    p108 = re.compile(r"^\s*(ip mtu|mtu)\s+(?P<mtu>\d+)")

    # ip flow monitor m4in sampler fnf_sampler input
    p109 = re.compile(
        r"^ip +flow +monitor +(?P<flow_monitor_in_sampler>[\w]+) +sampler +(?P<input_sampler>[\w]+) +input$"
    )

    #  ip flow monitor m4out sampler fnf_sampler output
    p110 = re.compile(
        r"^ip +flow +monitor +(?P<flow_monitor_out_sampler>[\w]+) +sampler +(?P<output_sampler>[\w]+) +output$"
    )

    # ip pim sparse-dense-mode
    p111 = re.compile(r"^ip +pim +(?P<pim_mode>[\S]+)$")

    # service-policy type queueing output 2p6q
    p112 = re.compile(r"^service-policy +type +(?P<policy_type>[\S]+) +output +(?P<output_name>[\S]+)$")

    # duplex full / duplex half / duplex auto
    p111_1 = re.compile(r"^duplex\s+(?P<duplex>(full|half|auto))$")

    # below matches
    # dialer pool-member 1
    # pppoe-client dial-pool-number 1
    p112_1 = re.compile(r"^(pppoe-client dial-pool-number|dialer (pool-member|pool))\s(?P<pool_number>\d+)$")

    # matches if standby or vrrp is visible in config
    p113 = re.compile(r"(standby|vrrp)")

    # ppp chap hostname hostname
    p114 = re.compile(r"^ppp chap hostname\s(?P<chap_hostname>.*)$")

    # ppp chap password 0 password
    # ppp chap password 7 08345F4B1B48
    p115 = re.compile(r"^ppp chap password\s(?P<chap_encryption>\d+)\s+(?P<chap_encryption_string>.*)$")

    # ppp pap sent-username cisco password myfirstpassword
    p116 = re.compile(r"^ppp pap sent-username\s(?P<pap_username>.*?)(?=\s)\spassword\s(?P<pap_password>.*)$")

    # pppoe-client ppp-max-payload 1500
    p117 = re.compile(r"^pppoe-client ppp-max-payload\s(?P<pppoe_max_payload>\d+)$")

    # ip helper-address 158.67.245.51
    p118 = re.compile(r"^ip\shelper-address\s(?P<ip_helper>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$")

    # pvc 2/32
    p119 = re.compile(r"^pvc\s(?P<pvc_vp>\d+)\/(?P<pvc_vc>\d+)$")

    # ubr 1024 48
    p120 = re.compile(r"^ubr(\+|)\s(?P<ubr_settings>.*)$")

    # ip address negotiated
    p121 = re.compile(r"^ip address negotiated$")

    # vbr-nrt 128 256
    p122 = re.compile(r"^vbr-nrt\s(?P<vbr_nrt>.*)$")

    # hold-queue 500 in
    p123 = re.compile(r"^hold-queue\s(?P<hold_queue_in>\d+)\sin$")

    # hold-queue 200 out
    p124 = re.compile(r"^hold-queue\s(?P<hold_queue_out>\d+)\sout$")

    # ip flow monitor monitor_ipv4_out output
    p125 = re.compile(r"^ip\s+flow\s+monitor\s+(?P<flow_monitor_output>\S+)\s+output$")

    # ip dhcp snooping information option allow-untrusted
    p126 = re.compile(r"^ip +dhcp +snooping +information +option +allow-untrusted$")

    # no ip dhcp snooping information option allow-untrusted
    p127 = re.compile(r"^no +ip +dhcp +snooping +information +option +allow-untrusted$")

    p128 = re.compile(r"^(?P<fhrp_protocol>(standby|vrrp))\s+(?P<group_id>\d+)")
    # standby 20 authentication cisco

    p129 = re.compile(
        r"^(?P<fhrp_protocol>(standby|vrrp))\s+(?P<group_id>\d+)\s+authentication\s+(?P<encryption_string>\w+)$"
    )
    # vrrp 100 authentication md5 key-string 7 070C285F4D06

    p130 = re.compile(
        r"^(?P<fhrp_protocol>(standby|vrrp))\s+(?P<group_id>\d+)\s+authentication md5 key-string\s(?P<encryption_level>\d+)\s(?P<encryption_string>.*)$"
    )

    # vrrp 100 ip 1.1.1.2
    # standby 100 ip 1.1.1.2
    p131 = re.compile(r"^(?P<fhrp_protocol>(standby|vrrp))\s+(?P<group_id>\d+)\s+(ip|ipv4)\s+(?P<ips>.*)$")

    # vrrp 100 description hatseflats
    # standby 100 description hatseflats
    p132 = re.compile(
        r"^(?P<fhrp_protocol>(standby|vrrp))\s+(?P<group_id>\d+)\s+(description|name)\s+(?P<description>.*)$"
    )

    # vrrp 100 priority 90
    # standby 100 priority 90
    p133 = re.compile(r"^(?P<fhrp_protocol>(standby|vrrp))\s+(?P<group_id>\d+)\s+priority\s(?P<priority>\d+)$")

    # standby 1 timers msec 150 160
    p134 = re.compile(r"^(?P<fhrp_protocol>(standby))\s+(?P<group_id>\d+)\s+timers\s(?P<timers>.*)$")

    #  vrrp 110 timers advertise msec 50
    p135 = re.compile(r"^(?P<fhrp_protocol>(vrrp))\s+(?P<group_id>\d+)\s+timers advertise\s(?P<timers>.*)$")

    #  vrrp 110 timers learn
    p136 = re.compile(r"^(?P<fhrp_protocol>(vrrp))\s+(?P<group_id>\d+)\s+timers\s(?P<timers>learn)$")

    # we want to know if an interface disabled the default vrrp preempt.
    # no vrrp 120 preempt
    p137 = re.compile(r"^no (?P<fhrp_protocol>vrrp)\s+(?P<group_id>\d+)\s+preempt")

    # and for hsrp it must be explicitly defined if preempt should be used
    # standby 10 preempt
    p138 = re.compile(r"(?P<fhrp_protocol>standby)\s+(?P<group_id>\d+)\s+preempt")

    # media-type rj45
    p139 = re.compile(r"^media-type\s+(?P<media_type>.*)$")

    # find the service_instance
    # service instance 11 ethernet
    # service instance service instance trunk 1 ethernet
    p_find_service_instance = re.compile(
        r"^(service instance|service instance trunk|)\s(?P<service_instance>\d+) ethernet$"
    )

    # bridge-domain 11 split-horizon group 0
    p_service_instance_bridge_domain = re.compile(r"bridge-domain\s(?P<bridge_domain>\d+).*$")

    # recycle p7 pattern
    # encapsulation dot1q 11
    p_service_instance_dot1q = p7
    # service-policy input AutoQos-4.0-CiscoPhone-Input-Policy
    p_service_instance_service_policy = p59

    # description belongs to BDI15 TEST2
    p_service_instance_description = p2

    for line in data.splitlines():
        line = line.strip()

        # interface GigabitEthernet0
        m = p1.match(line)
        if m:
            interface = m.groupdict()["interface"]
            intf_dict = config_dict.setdefault("interfaces", {}).setdefault(interface, {})
            intf_dict["interface"] = interface
            continue

        try:
            # there are situations when a config contains the following:
            # !
            # ip vrf testvpn
            #  description PWN-Alert-VPN
            #  rd 10735:1
            # !
            # the description regex would match on this.
            # but since its not part of an interface intf_dict would not exist and crashes
            intf_dict
        except UnboundLocalError:
            continue

        # description ISE Controlled Port
        m = p2.match(line)
        if m:
            description = m.groupdict()["description"]
            intf_dict.update({"description": description})
            continue

        # vrf forwarding Mgmt-intf
        m = p3.match(line)
        if m:
            vrf = m.groupdict()["vrf"]
            intf_dict.update({"vrf": vrf})
            continue

        # # ip address 10.1.21.249 255.255.255.0
        m = p4.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update(
                {
                    "ipv4": {"ip": group["ip"], "netmask": group["netmask"]},
                }
            )

        # # ip address 10.1.21.249 255.255.255.0 secondary
        m = p4_1.match(line)
        if m:
            group = m.groupdict()
            if not intf_dict.get("ipv4_secondaries", False):
                intf_dict["ipv4_secondaries"] = {}
            intf_dict["ipv4_secondaries"][group["ip"]] = {
                "ip": group["ip"],
                "netmask": group["netmask"],
                "primary": False,
            }

        # ipv6 address 2001:db8:4:1::1/64
        m = p5.match(line)
        if m:
            group = m.groupdict()
            intf_dict.setdefault("ipv6", []).append(group["ipv6"])
            continue

        # shutdown
        m = p6.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"shutdown": True})
            continue

        # encapsulation dot1Q 201
        m = p7.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"encapsulation_dot1q": group["dot1q"]})
            continue

        # encapsulation ppp
        m = p7_1.match(line)
        if m:
            intf_dict.update({"encapsulation_ppp": True})
            continue

        # carrier-delay up 60
        # carrier-delay down 60
        m = p8.match(line)
        if m:
            group = m.groupdict()
            intf_dict.setdefault("carrier_delay", []).append(group["carrier_delay"])
            continue

        # negotiation auto
        # no negotiation auto
        m = p9.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"negotiation_auto": group["negotiation"] is None})
            continue

        # cdp enable
        m = p10.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"cdp": group["cdp"]})
            continue

        # no keepalive
        m = p11.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"keepalive": group["keepalive"] is None})
            continue

        # switchport access vlan 70
        m = p12.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"switchport_access_vlan": group["vlan"]})
            continue

        # switchport mode access
        m = p13.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"switchport_mode": group["switchport_mode"]})
            continue

        # switchport nonegotiate
        m = p14.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"switchport_nonegotiate": group["nonegotiate"]})
            continue

        # ip arp inspection limit rate 1024
        m = p15.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"ip_arp_inspection_limit_rate": group["rate"]})
            continue

        # load-interval 30
        m = p16.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"load_interval": group["load_interval"]})
            continue

        # authentication control-direction
        m = p17.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"authentication_control_direction": group["direction"]})
            continue

        # authentication event fail action next-method
        m = p18.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"authentication_event_fail_action": group["action"]})
            continue

        # authentication host-mode multi-auth
        m = p19.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"authentication_host_mode": group["host_mode"]})
            continue

        # authentication order dot1x mab
        m = p20.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"authentication_order": group["order"]})
            continue

        # authentication priority dot1x mab
        m = p21.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"authentication_priority": group["priority"]})
            continue

        # authentication port-control auto
        m = p22.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"authentication_port_control": group["port_control"]})
            continue

        # authentication periodic
        m = p23.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"authentication_periodic": True})
            continue

        # authentication timer reauthenticate server
        m = p24.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"authentication_timer_reauthenticate_server": True})
            continue

        # authentication timer inactivity 65535
        m = p24_1.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"authentication_timer_inactivity": group["inactivity"]})
            continue

        # authentication timer reauthenticate 6000
        m = p24_2.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"authentication_timer_reauthenticate": int(group["authentication_timer_reauthenticate"])})
            continue

        # authentication violation restrict
        m = p25.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"authentication_violation": group["violation"]})
            continue

        # authentication fallback dot1x
        m = p26.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"authentication_fallback": group["fallback"]})
            continue

        # mab
        m = p27.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"mab": True})
            continue

        # snmp trap mac-notification change added
        m = p28.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"snmp_trap_mac_notification_change_added": True})
            continue

        # snmp trap mac-notification change removed
        m = p29.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"snmp_trap_mac_notification_change_removed": True})
            continue

        # no snmp trap link-status
        m = p30.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"snmp_trap_link_status": False})
            continue

        # dot1x pae authenticator
        m = p31.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"dot1x_pae_authenticator": True})
            continue

        # dot1x timeout quiet-period 5
        m = p32.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"dot1x_timeout_quiet_period": group["quiet_period"]})
            continue

        # dot1x timeout server-timeout 10
        m = p33.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"dot1x_timeout_server_timeout": group["server_timeout"]})
            continue

        # dot1x timeout tx-period 5
        m = p34.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"dot1x_timeout_tx_period": group["tx_period"]})
            continue

        # spanning-tree portfast
        m = p35.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"spanning_tree_portfast": True})
            continue

        # spanning-tree bpduguard enable
        m = p36.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"spanning_tree_bpduguard": group["bpduguard"]})
            continue

        # ip dhcp snooping limit rate 100
        m = p37.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"ip_dhcp_snooping_limit_rate": group["rate"]})
            continue

        # ipv6 enable
        m = p38.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"ipv6_enable": True})
            continue

        # ip ospf 2 area 0
        # ipv6 ospf 1 area 0
        m = p39.match(line)
        if m:
            group = m.groupdict()
            ip = group["ip"]
            ospf = group["ospf"]
            area = group["area"]
            intf_dict.setdefault("{}_ospf".format(ip), {}).setdefault(ospf, {}).update({"area": area})
            continue

        # ospfv3 1 ipv6 area 0
        p40 = re.compile(r"^ospfv3 +(?P<ospfv3>[\d]+) +(?P<ip>ip|ipv6) +area +(?P<area>[\d]+)$")
        m = p40.match(line)
        if m:
            group = m.groupdict()
            ip = group["ip"]
            ospf = group["ospfv3"]
            area = group["area"]
            intf_dict.setdefault("{}_ospfv3".format(ip), {}).setdefault(ospf, {}).update({"area": area})
            continue

        # channel-group 1 mode active
        m = p41.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update(
                {
                    "channel_group": {"chg": int(group["group"]), "mode": group["mode"]},
                }
            )
            continue

        # power inline port priority high
        m = p42.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"power_inline_port_priority": group["power_priority"]})

        # power inline never|static
        m = p43.match(line)
        if m:
            group = m.groupdict()
            if group["max_watts"]:
                intf_dict.update(
                    {
                        "power_inline": {"state": group["state"], "max_watts": group["max_watts"]},
                    }
                )
            else:
                intf_dict.update(
                    {
                        "power_inline": {"state": group["state"]},
                    }
                )
            continue

        # spanning-tree bpdufilter enable
        m = p44.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"spanning_tree_bpdufilter": group["bpdufilter"]})
            continue

        # ip flow monitor IPv4NETFLOW input
        m = p45.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"flow_monitor_input": group["flow_monitor_input"]})
            continue

        # switchport protected
        m = p46.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"switchport_protected": True})
            continue

        # switchport block unicast
        m = p47.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"switchport_block_unicast": True})
            continue

        # switchport block multicast
        m = p48.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"switchport_block_multicast": True})
            continue

        # switchport trunk allowed vlan 820,900-905
        # switchport trunk allowed vlan add 905-908
        m = p49.match(line)
        if m:
            group = m.groupdict()
            if "switchport_trunk_vlans" in intf_dict:
                group["vlans"] = intf_dict["switchport_trunk_vlans"] + "," + group["vlans"]
            intf_dict.update({"switchport_trunk_vlans": group["vlans"]})
            continue

        # ip dhcp snooping trust
        m = p50.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"ip_dhcp_snooping_trust": True})
            continue

        # ip arp inspection trust
        m = p51.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"ip_arp_inspection_trust": True})
            continue

        # ip unnumbered Loopback0
        m = p52.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"src_ip": group["src_address"]})
            continue

        # tunnel mode mpls traffic-eng
        m = p53.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"tunnel_mode": group["tunnel_mode"]})
            continue

        # tunnel destination 2.2.2.2
        m = p54.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"tunnel_dst": group["tunnel_dst"]})
            continue

        if "autoroute announce" in line:
            intf_dict.update({"autoroute_announce": "enabled"})
        if "autoroute destination" in line:
            intf_dict.update({"autoroute_destination": "enabled"})

        # tunnel destination 2.2.2.2
        m = p55.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"tunnel_priority": [group["value"]]})
            continue

        # tunnel mpls traffic-eng bandwidth 500
        m = p56.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"tunnel_bandwidth": int(group["value"])})
            continue

        # tunnel mpls traffic-eng path-option 1 dynamic
        m = p57.match(line)
        if m:
            group = m.groupdict()
            sub_dict = intf_dict.setdefault("tunnel_path_option", {}).setdefault(group["value"], {})
            if group["path_type"] == "dynamic":
                sub_dict.update({"path_type": group["path_type"]})
            else:
                sub_dict.update({"path_type": "explicit"})
                sub_dict.update({"path_name": group["path_type"]})
            continue

        # mpls ip
        m = p58.match(line)
        if m:
            intf_dict.update({"mpls_ip": "enabled"})
            continue

        # service-policy input AutoQos-4.0-CiscoPhone-Input-Policy
        m = p59.match(line)
        if m:
            group = m.groupdict()
            input_policy = group["input_policy"]
            intf_dict.update({"input_policy": group["input_policy"]})
            continue

        # service-policy output AutoQos-4.0-Output-Policy
        m = p60.match(line)
        if m:
            group = m.groupdict()
            output_policy = group["output_policy"]
            intf_dict.update({"output_policy": group["output_policy"]})

        # switchport port-security mac-address sticky 1020.4bb1.6f2f
        m = p61.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"mac_address_sticky": group["value"]})
            continue

        # source template USER_NoAuth
        m = p62.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"source_template": group["template"]})
            continue

        # host-reachability protocol bgp
        m = p63.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"host_reachability_protocol": group["protocol"]})
            continue

        # source-interface loopback1
        m = p64.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"source_interface": group["src_intf"]})
            continue

        # member vni 20011 ingress-replication
        m = p65.match(line)
        if m:
            member_vni = intf_dict.setdefault("member_vni", {})
            group = m.groupdict()
            member_vni.update({group["vni"]: {"ingress_replication": {"enabled": True}}})
            continue

        # member vni 20012 mcast-group 224.1.1.1
        m = p66.match(line)
        if m:
            member_vni = intf_dict.setdefault("member_vni", {})
            group = m.groupdict()
            member_vni.update({group["vni"]: {"mcast_group": group["ip"]}})
            continue

        # member vni 20011 ingress-replication local-routing
        m = p67.match(line)
        if m:
            member_vni = intf_dict.setdefault("member_vni", {})
            group = m.groupdict()
            member_vni.update({group["vni"]: {"ingress_replication": {"enabled": True}, "local_routing": True}})
            continue

        # member vni 20011
        m = p68.match(line)
        if m:
            member_vni = intf_dict.setdefault("member_vni", {})
            group = m.groupdict()
            vni = group["vni"]
            continue

        # ingress-replication 1.1.1.1
        m = p69.match(line)
        if m:
            member_vni = intf_dict.setdefault("member_vni", {})
            group = m.groupdict()
            member_vni.update({vni: {"ingress_replication": {"enabled": True, "remote_peer_ip": group["ip"]}}})
            continue

        # member vni 20012 mcast-group 224.1.1.1 local-routing
        m = p70.match(line)
        if m:
            member_vni = intf_dict.setdefault("member_vni", {})
            group = m.groupdict()
            member_vni.update({group["vni"]: {"mcast_group": group["ip"], "local_routing": True}})
            continue

        # member vni 30000 vrf red
        m = p71.match(line)
        if m:
            member_vni = intf_dict.setdefault("member_vni", {})
            group = m.groupdict()
            member_vni.update({group["vni"]: {"vrf": group["vrf"]}})
            continue

        # ip access-group DELETE_ME in ; ip access-group TEST-OUT out
        m = p72.match(line)
        if m:
            acl = intf_dict.setdefault("acl", {})
            group = m.groupdict()
            if group["direction"] == "in":

                inbound_dict = acl.setdefault("inbound", {})
                inbound_dict["acl_name"] = group["acl_name"]
                inbound_dict["direction"] = group["direction"]
                continue

            elif group["direction"] == "out":
                outbound_dict = acl.setdefault("outbound", {})
                outbound_dict["acl_name"] = group["acl_name"]
                outbound_dict["direction"] = group["direction"]
                continue

        # lisp mobility 20_1_1_0-global-IPV4
        m = p73.match(line)
        if m:
            lisp_mobility = m.groupdict()["lisp_mobility"]
            intf_dict.update({"lisp_mobility": lisp_mobility})
            continue

        # trust device cisco-phone / trust device ip-camera
        m = p74.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"trust_device": group["trust_device"]})
            continue

        # ipv6 destination-guard attach-policy Univ-v6-IPDG-Policy1
        m = p75.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"ipv6_destination_guard_attach_policy": group["ipv6_destination_guard_attach_policy"]})
            continue

        # ipv6 source-guard attach-policy Univ-v6-IPSG-Policy2
        m = p76.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"ipv6_source_guard_attach_policy": group["ipv6_source_guard_attach_policy"]})
            continue

        # spanning-tree portfast trunk
        m = p77.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"spanning_tree_portfast_trunk": True})
            continue

        # ipv6 nd raguard attach-policy Univ_IPv6_RA_Policy_Host
        m = p78.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"ipv6_nd_raguard_attach_policy": group["ipv6_nd_raguard_attach_policy"]})
            continue

        # device-tracking attach-policy IPDT_POLICY
        m = p79.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"device_tracking_attach_policy": group["device_tracking_attach_policy"]})
            continue

        # stackwise-virtual link 1
        m = p80.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"stackwise_virtual_link": int(group["stackwise_virtual_link"])})
            continue

        # stackwise-virtual dual-active-detection
        m = p81.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"dual_active_detection": group["dual_active_detection"] == "dual-active-detection"})
            continue

        # ip flow monitor monitor_ipv4_out output
        m = p82.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"flow_monitor_output": group["flow_monitor_output"]})
            continue

        # ip dhcp snooping information option allow-untrusted
        m = p83.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"ip_dhcp_snooping_information_option_allow_untrusted": True})
            continue

        # ip dhcp snooping information option allow-untrusted
        m = p84.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"ip_dhcp_snooping_information_option_allow_untrusted": False})
            continue

        # ipv6 flow monitor monitor_ipv6_in input
        m = p85.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"flow_monitor_input_v6": group["flow_monitor_input_v6"]})
            continue

        # ipv6 flow monitor monitor_ipv6_out output
        m = p86.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"flow_monitor_output_v6": group["flow_monitor_output_v6"]})
            continue

        # speed  25000
        m = p87.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"speed": int(group["speed"])})
            continue

        # speed  nonegotiate
        m = p88.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"speed_nonegotiate": True})
            continue

            # isis network point-to-point
        m = p89.match(line)
        if m:
            group = m.groupdict()
            intf_dict.setdefault("isis", {}).setdefault("network", group["isis_network"])
            continue

        # isis metric 22 level-1
        # isis metric 22 level-2
        m = p90.match(line)
        if m:
            group = m.groupdict()
            intf_dict.setdefault("isis", {}).setdefault("ipv4", {}).setdefault("level", {}).setdefault(
                group["isis_v4_level"], {}
            ).setdefault("metric", int(group["isis_v4_metric"]))
            continue

        # isis ipv6 metric 33 level-1
        # isis ipv6 metric 22 level-2
        m = p91.match(line)
        if m:
            group = m.groupdict()
            intf_dict.setdefault("isis", {}).setdefault("ipv6", {}).setdefault("level", {}).setdefault(
                group["isis_v6_level"], {}
            ).setdefault("metric", int(group["isis_v6_metric"]))
            continue

        # switchport trunk native vlan 101
        m = p92.match(line)
        if m:
            group = m.groupdict()
            intf_dict["switchport_trunk_native_vlan"] = int(m.groupdict()["switchport_trunk_native_vlan"])
            continue

        # access-session host-mode multi-host
        m = p93.match(line)
        if m:
            intf_dict["access_session_host_mode"] = m.groupdict()["access_session_host_mode"]
            continue

        # access-session closed
        m = p94.match(line)
        if m:
            intf_dict["access_session"] = m.groupdict()["access_session"]
            continue

        # access-session port-control auto
        m = p95.match(line)
        if m:
            intf_dict["access_session_port_control"] = m.groupdict()["access_session_port_control"]
            continue

        # dot1x pae both
        m = p96.match(line)
        if m:
            intf_dict["dot1x_pae"] = m.groupdict()["dot1x_pae"]
            continue

        # dot1x timeout supp-timeout 87
        m = p97.match(line)
        if m:
            intf_dict["dot1x_timeout_supp_timeout"] = int(m.groupdict()["dot1x_timeout_supp_timeout"])
            continue

        # dot1x max-req 6
        m = p98.match(line)
        if m:
            intf_dict["dot1x_max_req"] = int(m.groupdict()["dot1x_max_req"])
            continue

        # dot1x authenticator eap profile Self
        m = p99.match(line)
        if m:
            intf_dict["dot1x_authenticator_eap_profile"] = m.groupdict()["dot1x_authenticator_eap_profile"]
            continue

        # dot1x timeout held-period 63
        m = p100.match(line)
        if m:
            intf_dict["dot1x_timeout_held_period"] = int(m.groupdict()["dot1x_timeout_held_period"])
            continue

        # dot1x credentials EAPTLSCRED-IOSCA
        m = p101.match(line)
        if m:
            intf_dict["dot1x_credentials"] = m.groupdict()["dot1x_credentials"]
            continue

        # dot1x supplicant eap profile Self
        m = p102.match(line)
        if m:
            intf_dict["dot1x_supplicant_eap_profile"] = m.groupdict()["dot1x_supplicant_eap_profile"]
            continue

        # macsec
        m = p103.match(line)
        if m:
            intf_dict.update({"macsec_enabled": True})
            continue

        # macsec access-control should-secure
        m = p104.match(line)
        if m:
            intf_dict["macsec_access_control"] = m.groupdict()["macsec_access_control"]
            continue

        # mka policy MKAPolicy
        m = p105.match(line)
        if m:
            intf_dict["mka_policy"] = m.groupdict()["mka_policy"]
            continue

        # mka pre-shared-key key-chain KCP256
        m = p106.match(line)
        if m:
            intf_dict["mka_primary_keychain"] = m.groupdict()["mka_primary_keychain"]
            continue

        # mka pre-shared-key key-chain KCP256 fallback-key-chain KCF256
        m = p107.match(line)
        if m:
            intf_dict["mka_primary_keychain"] = m.groupdict()["mka_primary_keychain"]
            intf_dict["mka_fallback_keychain"] = m.groupdict()["mka_fallback_keychain"]
            continue

        # ip mtu 1468
        m = p108.match(line)
        if m:
            intf_dict["mtu"] = int(m.groupdict()["mtu"])
            continue

        # ip flow monitor m4in sampler fnf_sampler input
        m = p109.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"flow_monitor_in_sampler": group["flow_monitor_in_sampler"]})
            intf_dict.update({"input_sampler": group["input_sampler"]})
            continue

        # ip flow monitor m4out sampler fnf_sampler output
        m = p110.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"flow_monitor_out_sampler": group["flow_monitor_out_sampler"]})
            intf_dict.update({"output_sampler": group["output_sampler"]})
            continue

        # ip pim sparse-dense-mode
        m = p111.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"pim_mode": group["pim_mode"]})
            continue

        # service-policy type queuing output 2p6q
        m = p112.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"policy_type": group["policy_type"], "output_name": group["output_name"]})
            continue

        # duplex full/duplex half
        m = p111_1.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"duplex": group["duplex"]})
            continue

        # dialer pool-member 1
        # pppoe-client dial-pool-number 1
        m = p112_1.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"dialer_pool": group["pool_number"]})
            continue

        # set defaultdict fhrps if standby or vrrp is visible in the interface configuration
        m = p113.match(line)
        if m:
            intf_dict.setdefault("fhrps", {})

        # ppp chap hostname hostname
        m = p114.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"chap_hostname": group["chap_hostname"]})
            continue

        # ppp chap password 0 password
        # ppp chap password 7 08345F4B1B48
        m = p115.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update(
                {
                    "chap_password": group["chap_encryption_string"],
                    "chap_encryption": int(group["chap_encryption"]),
                }
            )
            continue

        # ppp pap sent-username cisco password myfirstpassword
        m = p116.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update(
                {
                    "pap_username": group["pap_username"],
                    "pap_password": group["pap_password"],
                }
            )
            continue

        # pppoe-client ppp-max-payload 1500
        m = p117.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"pppoe_max_payload": int(group["pppoe_max_payload"])})
            continue

        # ip helper-address 158.67.245.51
        m = p118.match(line)
        if m:
            group = m.groupdict()
            if not intf_dict.get("ip_helpers", False):
                intf_dict["ip_helpers"] = []
            intf_dict["ip_helpers"].append(group["ip_helper"])
            continue

        # pvc 2/32
        m = p119.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update(
                {
                    "pvc_vp": int(group["pvc_vp"]),
                    "pvc_vc": int(group["pvc_vc"]),
                }
            )
            continue

        # ubr 1024 48
        m = p120.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"pvc_ubr": group["ubr_settings"]})
            continue

        # ip address negotiated
        m = p121.match(line)
        if m:
            intf_dict.update({"ip_negotiated": True})
            continue

        # vbr-nrt 128 256
        m = p122.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"pvc_vbr_nrt": group["vbr_nrt"]})
            continue

        # hold-queue 500 in
        m = p123.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"hold_queue_in": int(group["hold_queue_in"])})
            continue

        # hold-queue 200 out
        m = p124.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"hold_queue_out": int(group["hold_queue_out"])})
            continue

        # ip flow monitor monitor_ipv4_out output
        m = p125.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"flow_monitor_output": group["flow_monitor_output"]})
            continue

        # ip dhcp snooping information option allow-untrusted
        m = p126.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"ip_dhcp_snooping_information_option_allow_untrusted": True})
            continue

        # no ip dhcp snooping information option allow-untrusted
        m = p127.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"ip_dhcp_snooping_information_option_allow_untrusted": False})
            continue

        # FROM HERE ALL FHRP
        m = p128.match(line)
        if m:
            group = m.groupdict()
            if not intf_dict["fhrps"].get(group["group_id"], False):
                intf_dict["fhrps"].update(
                    {
                        group["group_id"]: {
                            "protocol": "hsrp" if "standby" in group["fhrp_protocol"] else "vrrp",
                            "group_id": group["group_id"],
                        }
                    }
                )
                # dont use continue here otherwise
                # it wont match the other fhrp settings

        # standby 20 authentication cisco
        m = p129.match(line)
        if m:
            group = m.groupdict()
            intf_dict["fhrps"][group["group_id"]].update({"encryption_string": group["encryption_string"]})
            continue

        # vrrp 100 authentication md5 key-string 7 070C285F4D06
        m = p130.match(line)
        if m:
            group = m.groupdict()
            intf_dict["fhrps"][group["group_id"]].update(
                {"encryption_level": group["encryption_level"], "encryption_string": group["encryption_string"]}
            )
            continue

        # vrrp 100 ip 1.1.1.2
        # standby 100 ip 1.1.1.2
        m = p131.match(line)
        if m:
            group = m.groupdict()
            if not intf_dict["fhrps"][group["group_id"]].get("ips", False):
                intf_dict["fhrps"][group["group_id"]]["ips"] = []
            intf_dict["fhrps"][group["group_id"]]["ips"].append(group["ips"])
            continue

        # vrrp 100 description hatseflats
        # standby 100 description hatseflats
        m = p132.match(line)
        if m:
            group = m.groupdict()
            intf_dict["fhrps"][group["group_id"]].update({"fhrp_description": group["description"]})
            continue

        # vrrp 100 priority 90
        # standby 100 priority 90
        m = p133.match(line)
        if m:
            group = m.groupdict()
            intf_dict["fhrps"][group["group_id"]].update({"priority": group["priority"]})
            continue

        # standby 1 timers msec 150 160
        m = p134.match(line)
        if m:
            group = m.groupdict()
            intf_dict["fhrps"][group["group_id"]].update(
                {
                    "hsrp_timers": group["timers"],
                }
            )
            continue

        # vrrp 110 timers advertise msec 50
        m = p135.match(line)
        if m:
            group = m.groupdict()
            intf_dict["fhrps"][group["group_id"]].update(
                {
                    "vrrp_timers": group["timers"],
                }
            )
            continue

        # vrrp 110 timers learn
        m = p136.match(line)
        if m:
            group = m.groupdict()
            intf_dict["fhrps"][group["group_id"]].update({"vrrp_learn": True if "learn" in group["timers"] else False})
            continue

        # we want to know if an interface disabled the default vrrp preempt.
        # no vrrp 120 preempt
        m = p137.match(line)
        if m:
            group = m.groupdict()
            intf_dict["fhrps"][group["group_id"]].update({"vrrp_preempt": False})
            continue

        # for hsrp it must be explicitly defined if preempt should be used
        # standby 10 preempt
        m = p138.match(line)
        if m:
            group = m.groupdict()
            intf_dict["fhrps"][group["group_id"]].update({"hsrp_preempt": True})
            continue

        # media-type rj45
        m = p139.match(line)
        if m:
            group = m.groupdict()
            intf_dict.update({"media_type": group["media_type"]})
            continue

        m = p_find_service_instance.match(line)
        if m:
            service_instance = m.groupdict()["service_instance"]
            # create the service_instance dict
            if not intf_dict.get("service_instances", False):
                intf_dict["service_instances"] = {}
            intf_dict["service_instances"][service_instance] = {}
            intf_dict["service_instances"][service_instance]["service_instance"] = service_instance
            # service instance config is extra identented and needs to be kept together.
            # therefor we search for the block based on the service_instance_id
            #  service instance 11 ethernet
            #  encapsulation dot1q 11
            #  rewrite ingress tag pop 1 symmetric
            #  bridge-domain 11 split-horizon group 0
            # !
            regex = f"(service instance|service instance trunk)\s{service_instance}\sethernet(?P<service_instance_config>[\s\S]*?(?=\n.*?\!))"
            p_service_instance_config = re.compile(regex)
            service_instance_config = p_service_instance_config.findall(data)
            for line in service_instance_config[0][1].splitlines():
                line = line.strip()
                m = p_service_instance_bridge_domain.match(line)
                if m:
                    group = m.groupdict()
                    intf_dict["service_instances"][service_instance]["bridge_domain"] = group["bridge_domain"]
                    continue

                m = p_service_instance_dot1q.match(line)
                if m:
                    group = m.groupdict()
                    intf_dict["service_instances"][service_instance]["dot1q"] = group["dot1q"]

                    if "," in group["dot1q"] or "-" in group["dot1q"]:
                        intf_dict["service_instances"][service_instance]["service_instance_trunked"] = True
                    else:
                        intf_dict["service_instances"][service_instance]["service_instance_trunked"] = False
                    continue

                m = p_service_instance_service_policy.match(line)
                if m:
                    group = m.groupdict()
                    intf_dict["service_instances"][service_instance]["service_policy"] = group["input_policy"]
                    continue

                m = p_service_instance_description.match(line)
                if m:
                    group = m.groupdict()
                    intf_dict["service_instances"][service_instance]["description"] = group["description"]
                    continue

    # if an interface has service_instances
    # we unset the global encapsulation_dot1q
    # we unset the global description
    # this is due that the service instances have there encapsulation value and description
    try:
        if intf_dict.get("service_instances", False) and intf_dict.get("encapsulation_dot1q", False):
            del intf_dict["encapsulation_dot1q"]
            del intf_dict["description"]
    except NameError:
        pass

    all_values = get_interface_information(config_dict)

    return all_values


def get_interface_information(d):
    interface_data = []
    for key, values in d["interfaces"].items():
        interface_data.append(values)
    return interface_data
