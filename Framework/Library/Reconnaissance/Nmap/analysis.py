def analysis_service(port):
    if "@portid" in port:
        port_service = int(port['@portid'])
    else: port_service = 0
    if "@protocol" in port:
        protocol_service = port['@protocol']
    else: protocol_service = ""

    if "@version" in port['service']:
        version_service = port['service']['@version']
    else: version_service = 0.0
    name_service = port['service']['@name']
    if "@product" in port['service']:
        product_service = port['service']['@product']
    else: product_service = 0.0

    return {
                        "name" : name_service,
                        "product" : product_service,
                        "version" : version_service,
                        "port" :  port_service,
                        "protocol" : protocol_service
                    }