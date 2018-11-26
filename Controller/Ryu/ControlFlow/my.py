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







