
from ocelot.cpbd.elements.sbend import SBend
from ocelot.cpbd.elements.drift import Drift
from ocelot.cpbd.transformations.transfer_map import TransferMap, TMTypes


def compare_lists(cur_list, truth_list):
    if len(cur_list) != len(truth_list):
        return False
    return all(tm_type == truth_tm_type for tm_type, truth_tm_type in zip(cur_list, truth_list))


def test_get_section_tms_with_sbend():
    ele = SBend(l=0.200330283531, angle=-0.1109740393, e1=-0.05548702, e2=-0.05548702, tilt=0.0, fint=0.0, eid='BL.48I.I1', tm=TransferMap)

    # start_l = 0.0 and start + delta > max length
    tms = ele.get_section_tms(start_l=0.0, delta_l=1.0)
    assert compare_lists([tm.tm_type for tm in tms], [TMTypes.ENTRANCE, TMTypes.MAIN, TMTypes.EXIT])

    # start_l = 0.0 and start + delta < max length
    tms = ele.get_section_tms(start_l=0.0, delta_l=0.1)
    assert compare_lists([tm.tm_type for tm in tms], [TMTypes.ENTRANCE, TMTypes.MAIN])

    # 0 < start_l < max length and start_l + delta_length > max length
    tms = ele.get_section_tms(start_l=0.1, delta_l=1.0)
    assert compare_lists([tm.tm_type for tm in tms], [TMTypes.MAIN, TMTypes.EXIT])

    # 0 < start_l < max length and start_l + delta_length = max length
    tms = ele.get_section_tms(start_l=0.1, delta_l=0.200330283531000001)
    assert compare_lists([tm.tm_type for tm in tms], [TMTypes.MAIN, TMTypes.EXIT])

    #  0 < start_l < max length and  start_l + delta_length < max length
    tms = ele.get_section_tms(start_l=0.05, delta_l=0.15)
    assert compare_lists([tm.tm_type for tm in tms], [TMTypes.MAIN])


def test_get_section_tms_with_drift():
    ele = Drift(l=0.1586084195, eid='D_103', tm=TransferMap)

    # start_l = 0.0 and start + delta > max length
    tms = ele.get_section_tms(start_l=0.0, delta_l=1.0)
    assert compare_lists([tm.tm_type for tm in tms], [TMTypes.MAIN])

    # start_l = 0.0 and start + delta < max length
    tms = ele.get_section_tms(start_l=0.0, delta_l=0.1)
    assert compare_lists([tm.tm_type for tm in tms], [TMTypes.MAIN])

    # 0 < start_l < max length and start_l + delta_length > max length
    tms = ele.get_section_tms(start_l=0.1, delta_l=1.0)
    assert compare_lists([tm.tm_type for tm in tms], [TMTypes.MAIN])

    # 0 < start_l < max length and start_l + delta_length = max length
    tms = ele.get_section_tms(start_l=0.1, delta_l=0.1586084195)
    assert compare_lists([tm.tm_type for tm in tms], [TMTypes.MAIN])

    #  0 < start_l < max length and  start_l + delta_length < max length
    tms = ele.get_section_tms(start_l=0.05, delta_l=0.15)
    assert compare_lists([tm.tm_type for tm in tms], [TMTypes.MAIN])
