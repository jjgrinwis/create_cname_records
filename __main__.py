"""A Python Pulumi program"""

import pulumi
import pulumi_akamai as akamai


def create_cname_records(x):
    # special function to split our TXT string and add it to EdgeDNS
    records = []

    for record in x:
        items = record.split()
        akamai.DnsRecord(
            items[1],
            recordtype='CNAME',
            ttl=int(items[3]),
            zone="pulumi.nl",
            name=items[1],
            targets=[items[4]]  # should be a list
        )

        records.append(items[1])

    return(records)


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
