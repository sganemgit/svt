from GenericLinkManagement import GenericLinkManagement


class LmLoopbackWithLpFlow(GenericLinkManagement):
	

	def run(self):

		while not timer.expired():
			for dut,lp in self.pairs:
				for fec in self.fec_dict[phy_type]:
					try:
						self.configure_link(dut, lp, phy_type, fec)
					except Exception as e:
						raise e
					for reset in resets:
						self.set_loopback_mode(dut)
						self.check_link(dut, lp)
						self.run_traffic(dut, lp)

						self.reset_both_sides(dut, lp, reset)


						if reset in self.loopback_destructive_resets_list:

							self.run_traffic()

						else:
							self.disable_loopback_mode(dut, lp)


							self.check_link(dut, lp)

