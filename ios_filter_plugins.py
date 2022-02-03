
#!/usr/bin/python3

class FilterModule(object):

    def ios_uptime_facts(self, ios_command_results): # show version | include uptime
        import re;
        if re.search("uptime\sis\s(.*)",ios_command_results,re.I):
            return re.search("uptime\sis\s(.*)",ios_command_results,re.I)[1];
        else:
            return None;

    def ios_interface_facts(self, ios_command_results): # show runnig-config
        interface_configuration_facts = list();
        interface_configuration_flag = False;
        for line in ios_command_results.split("\n"):
            import re;
            if re.search("interface\s[\w\d\/]+", line):
                interface_configuration_flag = True;
                interface_configuration = dict();
                interface_configuration["name"] = re.search("interface\s([\w\d\/]+)", line)[1];
            if interface_configuration_flag:
                if re.search("\sip\saddress\s([\d\.\s]+)", line):
                    interface_configuration["ip"] = re.search("\sip\saddress\s([\d\.]+)\s([\d\.]+)", line)[1];
                    interface_configuration["mask"] = re.search("\sip\saddress\s([\d\.]+)\s([\d\.]+)", line)[2];
                if re.search("\sshutdown", line):
                    interface_configuration["state"] = "shutdown";
                if re.search("!", line):
                    interface_configuration_flag = False;
                    interface_configuration_facts.append(interface_configuration);
        return interface_configuration_facts;

    def ios_ospf_facts(self, ios_command_results): # show runnig-config
        ospf_configuration_facts = list();
        ospf_configuration_flag = False;
        for line in ios_command_results.split("\n"):
            import re;
            if re.search("router\sospf\s[\d\.]+", line):
                ospf_configuration_flag = True;
                ospf_configuration = dict();
                ospf_configuration["ospf_process_id"] = re.search("router\sospf\s([\d\.]+)", line)[1];
                ospf_network_configuration_list = list();
            if ospf_configuration_flag:
                if re.search("\snetwork\s([\d\.]+)\s([\d\.]+)\sarea\s([\d\.]+)", line):
                    ospf_network_configuration = dict();
                    ospf_network_configuration["ospf_network_address"] = re.search("\snetwork\s([\d\.]+)\s([\d\.]+)\sarea\s([\d\.]+)", line)[1];
                    ospf_network_configuration["ospf_wildcard_mask"] = re.search("\snetwork\s([\d\.]+)\s([\d\.]+)\sarea\s([\d\.]+)", line)[2];
                    ospf_network_configuration["ospf_area_id"] = re.search("\snetwork\s([\d\.]+)\s([\d\.]+)\sarea\s([\d\.]+)", line)[3];
                    ospf_network_configuration_list.append(ospf_network_configuration);
                if re.search("!", line):
                    ospf_configuration["ospf_network_configuration"] = ospf_network_configuration_list;
                    ospf_configuration_flag = False;
                    ospf_configuration_facts.append(ospf_configuration);
        return ospf_configuration_facts;

    def filters(self):
        return {"ios_uptime_facts": self.ios_uptime_facts, "ios_interface_facts": self.ios_interface_facts, "ios_ospf_facts": self.ios_ospf_facts};
