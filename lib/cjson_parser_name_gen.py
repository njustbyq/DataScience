from __future__ import print_function
import json
import os
import re
from sys import prefix

# parse json
def dict_generator(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                if len(value) == 0:
                    yield pre + [key, '{}']
                else:
                    for d in dict_generator(value, [key]):
                        yield d
            elif isinstance(value, list):
                if len(value) == 0:                   
                    yield pre + [key, '[]']
                else:
                    for v in value:
                        for d in dict_generator(v, [key]):
                            yield d
            elif isinstance(value, tuple):
                if len(value) == 0:
                    yield pre+[key, '()']
                else:
                    for v in value:
                        for d in dict_generator(v, [key]):
                            yield d
            else:
                yield pre + [key, value]
    else:
        yield pre + [indict]

if __name__ == "__main__":
    with open("context.json",'r', encoding='UTF-8') as f:
        sValue = json.load(f)

    # turn json file into list
    list1 = []
    my_file = open(os.getcwd() + "/cjson_parser_name.h", "w")

    # FIXME: The decimal point can be removed from DECHUN
    for i in dict_generator(sValue):
        for j in i:
            if isinstance(j, str):
                list1.append(j.replace('.', '_'))
            elif isinstance(j, list):
                for k in j:
                    if isinstance(k, str):
                        list1.append(k.replace('.', '_'))

    # Remove duplicate element
    Large_list = []
    for i in range(len(list1)):
        opt = list1[i].upper()
        Large_list.append(opt)
    
    seen = set()
    result = []
    for item in Large_list:
        if item not in seen:
            seen.add(item)
            result.append(item)
    #print(result) 

    # Remove elements from "actions" to "pipelines"
    actions_index = result.index('ACTIONS')
    pipelines_index = result.index('PIPELINES')

    # FIXME: The filename index can be removed from DECHUN
    filename_index = result.index('FILENAME')
    del result[filename_index + 1 : filename_index + 2]
    del result[actions_index + 1 : pipelines_index]
    advertising_index_start = result.index("TAURUS/SWITCH_TAURUS_P4I")
    advertising_index_end = result.index("HTTPS://GITHUB_COM/P4LANG/P4C")
    del result[advertising_index_start : advertising_index_end + 1]
    result.remove('[]')
    #print(result)

    # Remove unwanted string from the json element
    tuple_index_start = result.index('TUPLE_0_F0')
    tuple_index_end = result.index('TUPLE_0_F15')
    for item in result[tuple_index_start : tuple_index_end + 1]:
        result.remove(item)
        fix = item.replace('TUPLE_', '')
        result.append(fix)
    
    igmd_index_start = result.index("IG_MD_0__PEW_INFO_RSV0")
    igmd_index_end = result.index("IG_MD_0__GLOBAL_INFO_INNER_VLAN2_VLD80")
    for item in result[igmd_index_start : igmd_index_end + 1]:
        result.remove(item)
        fix = item.replace('IG_MD_0__', '')
        result.append(fix)
    
    egress_index_start = result.index("INGRESS_INTRINSIC_METADATA_FOR_TM_T_UCAST_EGRESS_PORT")
    egress_index_end = result.index("EGRESS_INTRINSIC_METADATA_FOR_OUTPUT_PORT_T_FORCE_TX_ERROR")
    for item in result[egress_index_start : egress_index_end + 1]:
        opt = ""
        prefix = "EGRESS_"
        result.remove(item)
        fix_egress = item.replace("EGRESS_INTRINSIC_METADATA_", '')
        opt = prefix + fix_egress
        result.append(opt)
    
    ingress_index_start = result.index("EGRESS_INGRESS_INTRINSIC_METADATA_FOR_TM_T_UCAST_EGRESS_PORT")
    ingress_index_end = result.index("EGRESS_INGRESS_INTRINSIC_METADATA_FOR_DEPARSER_T_MIRROR_TYPE")
    for item in result[ingress_index_start : ingress_index_end + 1]:
        opt = ""
        prefix = "INGRESS_"
        result.remove(item)
        fix_ingress = item.replace("EGRESS_INGRESS_INTRINSIC_METADATA_", '')
        opt = prefix + fix_ingress
        result.append(opt)
    

    egress_index_start = result.index("INGRESS_EGRESS_FROM_PARSER_T_GLOBAL_TSTAMP")
    egress_index_end = result.index("INGRESS_EGRESS_FROM_PARSER_T_PARSER_ERR")
    for item in result[egress_index_start : egress_index_end + 1]:
        opt = ""
        prefix = "EGRESS_"
        result.remove(item)
        fix_egress = item.replace("INGRESS_EGRESS_", '')
        opt = prefix + fix_egress
        result.append(opt)
    #print(result)
    
    Little_list = []
    for i in range(len(result)):
        opt = result[i].lower()
        Little_list.append(opt)
    
     
    final_list = list(Little_list)

    # Recover String
    pew_index_start = final_list.index("pew_info_rsv0")
    global_index_end = final_list.index("global_info_inner_vlan2_vld80")
    for item in final_list[pew_index_start : global_index_end + 1]:
        opt = ""
        prefix = "ig_md_0._"
        final_list.remove(item)
        final_list.append(prefix + item)
    

    tuple_index_start = final_list.index("0_f0")
    tuple_index_end = final_list.index("0_f15")
    for item in final_list[tuple_index_start : tuple_index_end + 1]:
        opt = ""
        prefix = "tuple_0."
        fix = item.replace("0_", "")
        final_list.remove(item)
        final_list.append(prefix + fix)

    egress_deparser_index_start = final_list.index("egress_for_deparser_t_drop_ctl")
    egress_deparser_index_end = final_list.index("egress_for_deparser_t_coalesce_length")
    for item in final_list[egress_deparser_index_start : egress_deparser_index_end + 1]:
        opt = ""
        prefix = "egress_intrinsic_metadata_for_deparser_t."
        fix = item.replace("egress_for_deparser_t_", '')
        final_list.remove(item)
        final_list.append(prefix + fix)
    
    egress_parser_index_start = final_list.index("egress_from_parser_t_global_tstamp")
    egress_parser_index_end = final_list.index("egress_from_parser_t_parser_err")
    for item in final_list[egress_parser_index_start : egress_parser_index_end + 1]:
        opt = ""
        prefix = "egress_intrinsic_metadata_from_parser_t."
        fix = item.replace("egress_from_parser_t_", '')
        final_list.remove(item)
        final_list.append(prefix + fix)
    
    egress_port_index_start = final_list.index("egress_for_output_port_t_capture_tstamp_on_tx")
    egress_port_index_end = final_list.index("egress_for_output_port_t_force_tx_error")
    for item in final_list[egress_port_index_start : egress_port_index_end + 1]:
        opt = ""
        prefix = "egress_intrinsic_metadata_for_output_port_t."
        fix = item.replace("egress_for_output_port_t_", '')
        final_list.remove(item)
        final_list.append(prefix + fix)

    ingress_tm_index_start = final_list.index("ingress_for_tm_t_ucast_egress_port")
    ingress_tm_index_end = final_list.index("ingress_for_tm_t_rid")
    for item in final_list[ingress_tm_index_start : ingress_tm_index_end + 1]:
        opt = ""
        prefix = "ingress_intrinsic_metadata_for_tm_t."
        fix = item.replace("ingress_for_tm_t_", '')
        final_list.remove(item)
        final_list.append(prefix + fix)

    ingress_parser_index_start = final_list.index("ingress_from_parser_t_global_tstamp")
    ingress_parser_index_end = final_list.index("ingress_from_parser_t_parser_err")
    for item in final_list[ingress_parser_index_start : ingress_parser_index_end + 1]:
        opt = ""
        prefix = "ingress_intrinsic_metadata_from_parser_t."
        fix = item.replace("ingress_from_parser_t_", '')
        final_list.remove(item)
        final_list.append(prefix + fix)
    
    ingress_deparser_index_start = final_list.index("ingress_for_deparser_t_drop_ctl")
    ingress_deparser_index_end = final_list.index("ingress_for_deparser_t_mirror_type")
    for item in final_list[ingress_deparser_index_start : ingress_deparser_index_end + 1]:
        opt = ""
        prefix = "ingress_intrinsic_metadata_for_deparser_t."
        fix = item.replace("ingress_for_deparser_t_", '')
        final_list.remove(item)
        final_list.append(prefix + fix)

    #print(final_list)
    #print("************************************************************")
    

    define_list = list(final_list)
    # Rerange define_list
    pew_index_start = define_list.index("ig_md_0._pew_info_rsv0")
    global_index_end = define_list.index("ig_md_0._global_info_inner_vlan2_vld80")
    for item in define_list[pew_index_start : global_index_end + 1]:
        define_list.remove(item)
        fix = item.replace('ig_md_0._', '')
        define_list.append(fix)

    tuple_index_start = define_list.index('tuple_0.f0')
    tuple_index_end = define_list.index('tuple_0.f15')
    for item in define_list[tuple_index_start : tuple_index_end + 1]:
        define_list.remove(item)
        fix = item.replace('tuple_0.', '0_')
        define_list.append(fix)

    egress_deparser_index_start = define_list.index("egress_intrinsic_metadata_for_deparser_t.drop_ctl")
    egress_deparser_index_end = define_list.index("egress_intrinsic_metadata_for_deparser_t.coalesce_length")
    for item in define_list[egress_deparser_index_start : egress_deparser_index_end + 1]:
        define_list.remove(item)
        fix = item.replace("egress_intrinsic_metadata_for_deparser_t.", '')
        prefix = "egress_for_deparser_t_"
        define_list.append(prefix + fix)
    
    egress_parser_index_start = define_list.index("egress_intrinsic_metadata_from_parser_t.global_tstamp")
    egress_parser_index_end = define_list.index("egress_intrinsic_metadata_from_parser_t.parser_err")
    for item in define_list[egress_parser_index_start : egress_parser_index_end + 1]:
        define_list.remove(item)
        fix = item.replace("egress_intrinsic_metadata_from_parser_t.", '')
        prefix = "egress_for_parser_t_"
        define_list.append(prefix + fix)
    
    egress_port_index_start = define_list.index("egress_intrinsic_metadata_for_output_port_t.capture_tstamp_on_tx")
    egress_port_index_end = define_list.index("egress_intrinsic_metadata_for_output_port_t.force_tx_error")
    for item in define_list[egress_port_index_start : egress_port_index_end + 1]:
        define_list.remove(item)
        fix = item.replace("egress_intrinsic_metadata_for_output_port_t.", '')
        prefix = "egress_for_output_port_t_"
        define_list.append(prefix + fix)
    
    ingress_tm_index_start = define_list.index("ingress_intrinsic_metadata_for_tm_t.ucast_egress_port")
    ingress_tm_index_end = define_list.index("ingress_intrinsic_metadata_for_tm_t.rid")
    for item in define_list[ingress_tm_index_start : ingress_tm_index_end + 1]:
        define_list.remove(item)
        fix = item.replace("ingress_intrinsic_metadata_for_tm_t.", '')
        prefix = "ingress_for_tm_t_"
        define_list.append(prefix + fix)

    ingress_parser_index_start = define_list.index("ingress_intrinsic_metadata_from_parser_t.global_tstamp")
    ingress_parser_index_end = define_list.index("ingress_intrinsic_metadata_from_parser_t.parser_err")
    for item in define_list[ingress_parser_index_start : ingress_parser_index_end + 1]:
        define_list.remove(item)
        fix = item.replace("ingress_intrinsic_metadata_from_parser_t.", '')
        prefix = "ingress_from_parser_t_"
        define_list.append(prefix + fix)
    
    ingress_deparser_index_start = define_list.index("ingress_intrinsic_metadata_for_deparser_t.drop_ctl")
    ingress_deparser_index_end = define_list.index("ingress_intrinsic_metadata_for_deparser_t.mirror_type")
    for item in define_list[ingress_deparser_index_start : ingress_deparser_index_end + 1]:
        define_list.remove(item)
        fix = item.replace("ingress_intrinsic_metadata_for_deparser_t.", '')
        prefix = "ingress_for_deparser_t_"
        define_list.append(prefix + fix)

    #print(define_list)
    define_list.append("parser")
    final_list.append("parser")

    # Write define expressions into file
    opt1 = "/*---------------------------------------------------------------------- \n"
    opt2 = " * WARINING! EDIT THIS FILE IS FORBIDDEN! \n"
    opt3 = " * Any code change in this file will be lost when it is regenerated. \n"
    opt4 = " * Please edit corresponding json file to edit this file. \n"
    opt5 = " * \n"
    opt6 = " * @copyright    2021-2023 Jianling Semiconductor(C). All rights reserved. \n"
    opt7 = " *----------------------------------------------------------------------*/ \n"

    my_file.write(opt1)
    my_file.write(opt2)
    my_file.write(opt3)
    my_file.write(opt4)
    my_file.write(opt5)
    my_file.write(opt6)
    my_file.write(opt7)
    prefix = "#define CTX_JSON_"
    
    for key, val in zip(define_list, final_list):
        opt = ""
        opt =prefix + key.upper() + "_NODE  \"" + val + "\"\n" 
        my_file.write(opt)
    
    my_file.close()


