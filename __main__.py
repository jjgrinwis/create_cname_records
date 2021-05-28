"""A Python Pulumi program"""

import pulumi
import pulumi_akamai as akamai


def create_cname_records(x):
    # special function to split our DNS CNAME string for other stack and add it to EdgeDNS
    # for this demo we're using a prefconfigured zone pulumi.nl
    records = []

    # check if reference has any value at all
    if x:
        # we should pythonfy these for loops via list comprehension
        for property in x:
            for hostname in property:
                record = hostname.split()
                akamai.DnsRecord(
                    record[0],
                    recordtype='CNAME',
                    ttl=int(record[2]),
                    zone="pulumi.nl",
                    name=record[0],
                    targets=[record[3]]  # should be a list
                )

            records.append(record[0])

        return(records)
    else:
        pulumi.warn("empty stack reference, no records are being created")

    return None


# get the CNAME records to be created from other stack and select correct credentials
# $ pulumi config set akamai:dnsSection dns
# with different stacks we can destroy this stack when certificate has been approved
#
# stack_ref = pulumi.StackReference("jjgrinwis/property/betajam")
# this is again a Pulumi Output object so use apply() to get the real values
stack_ref = pulumi.StackReference("jjgrinwis/property/betajam")

txt_records = stack_ref.get_output(
    "target").apply(lambda x: create_cname_records(x))

pulumi.export("created records", txt_records)
