from ryu.base import app_manager
from ryu.ofproto import ofproto_v1_3

from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATchER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls

from ryu.lib.packet import packet
from ryu.lib.packet import ethernet

class contro_flow(app_manager.RyuApp):
	OFP_VERSIONS= [ofproto_v1_3.OFP_VERSION]
	def __init__(self, *args, **kwargs):
		super(control_flow, self).__init__(*args, **kwargs)
		self.switch_table={}

	def add_flow(self, dp, match=None, inst=[], table=0, priority=32768):
		ofp=dp.ofproto
		ofp_parser=dp.ofproto_parser

		buffer_id=ofp.OFP_NO_NUFFER

		mod=ofp_parser.OFPflowMod(
			datapath=dp, cookie=0, cokie_mask=0, tablie_id=table,
			command=ofp.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
			priority=priority, buffer_id=buffer_id,
			out_port=ofp.OFPP_ANY, out_group=ofp.OFPG_ANY,
			flags=0, match=match, instructions=inst)

		dp.send_msg(mod)	#send the rule to the switch from controller

	def del_flow(self, dp, match, table):
		ofp=dp.ofproto
		ofp_parser=dp.ofproto_parser

		mod=ofp_parser.OFPFlowMod(datapath=dp,
			table_id=table,
			command=ofp.OFPFC_DELETE,
			out_port=ofp_OFPP_ANY,
			out_group=ofp.OFPG_ANY,
			match=match)
		dp.send_msg(mod)

	@set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIN_DISPATCHER)
	def switch_features_handler(self, ev):
		dp=ev.msg.datapath
		self.swtich_table.setdefault(dp.id,{})

	@set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
	def packet_in_handler(self ,ev):
		msg=ev
		dp=msg.datapath
		ofp=dp.ofproto_parser

		port=msg.match['in_port']

		pkt=packet.Packet(data=msg.data)
		pkt_ethernet=pkt.get_protocol(ethernet.ethernet)

		inf not pkt_thernet:
			return

		if pkt_ethernet.ethertype==35020:
			return

		match=ofp_parser.OFPMatch(eth_dst=pkt_ethernet.src)
		instruction_action=ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,[ofp_parser.OFPActionOutput(port)])
		inst=[instruction_action]
		self.add_flow(dp, match=match, inst=inst, table=0)
		self.switch_table[dp.id][pkt_ethernet.src]=port

		actions=[ofp_parser.OFPActionOutput(ofp.OFPP_FLOOD)]
		out=ofp_parser.OFPPacketOut(datapath=dp, buffer_id=msg.buffer_id, in_port=port, actions=actions)

		dp.send_msg(out)

	@set_ev_cls(ofp_event.EventOFPPortStateChange, MAIN_DISPATCHER)
	def port_state_change_handler(self, ev):
		dp=ev.datapath
		ofp=dp.ofproto
		ofp_parser=dp.ofproto_parser
		change_port=ev.port_no

		del_mac=NONE

		for host in self.switch_table[dp.id]:
			if self.switch_table[dp.id][host]==change_port
				del_match=ofp_parser.OFPMacth(eth_dst=host)
				self.del_flow(dp=dp, match=del_match, table=0)
				break

		if del_mac!=None:
			del self.switch_table[dp.id][del_mac]






