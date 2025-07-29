from . import *
from .logger import logger, Verbosity
from pypamguard.core.filters import Filters, DateFilter, WhitelistFilter
import datetime

if __name__ == "__main__":

    d1 = datetime.datetime.fromtimestamp(1499572333281 / 1000, tz = datetime.UTC)
    d2 = datetime.datetime.fromtimestamp(1499572363281 / 1000, tz = datetime.UTC)

    pg_filters = Filters({
        # 'daterange': DateFilter(d1, d2, ordered=True),
        # 'uidlist': WhitelistFilter([2000006, 2000003])
    })

    # click_v4_test1_daterange = load_pamguard_binary_file("../tests/dataset/detectors/click/click_v4_test1.pgdf", json_path="click_v4_test1.json", filters=Filters({'daterange': DateFilter(datetime.datetime.fromtimestamp(1504477746918 / 1000, tz = datetime.UTC), datetime.datetime.fromtimestamp(1504477758412 / 1000, tz = datetime.UTC), ordered=True)}))


    # filterednoisemeasurement_v3_test1 = load_pamguard_binary_file("../tests/dataset/processing/filterednoisemeasurement/filterednoisemeasurement_v3_test1.pgdf", json_path="filterednoisemeasurement_v3_test1.json")

    # clicktriggerbackground = load_pamguard_binary_file("../tests/dataset/detectors/clicktriggerbackground/clicktriggerbackground_v0_test1.pgdf", json_path="clicktriggerbackground_v0_test1.json")
    # clicktriggerbackground_daterange = load_pamguard_binary_file("../tests/dataset/detectors/clicktriggerbackground/clicktriggerbackground_v0_test1.pgdf", json_path="clicktriggerbackground_v0_test1_datetime.json", filters=Filters({'daterange': DateFilter(datetime.datetime.fromtimestamp(1751975573249 / 1000, tz = datetime.UTC), datetime.datetime.fromtimestamp(1751975698249 / 1000, tz = datetime.UTC), ordered=True)}))
    # clicktriggerbackground_uidlist = load_pamguard_binary_file("../tests/dataset/detectors/clicktriggerbackground/clicktriggerbackground_v0_test1.pgdf", json_path="clicktriggerbackground_v0_test1_uidlist.json", filters=Filters({'uidlist': WhitelistFilter([2000028, 2000032])}))

    # spermwhaleipi_v1_test1 = load_pamguard_binary_file("../tests/dataset/spermwhaleipi/spermwhaleipi_v1_test1.pgdf", json_path="spermwhaleipi_v1_test1.json", filters=pg_filters)
    # spermwhaleipi_v1_test1_daterange = load_pamguard_binary_file("../tests/dataset/plugins/spermwhaleipi/spermwhaleipi_v1_test1.pgdf", json_path="spermwhaleipi_v1_test1_daterange.json", filters=Filters({'daterange': DateFilter(datetime.datetime.fromtimestamp(1751975639054 / 1000, tz = datetime.UTC), datetime.datetime.fromtimestamp(1751975732265 / 1000, tz = datetime.UTC), ordered=True)}))
    # spermwhaleipi_v1_test1_uidlist = load_pamguard_binary_file("../tests/dataset/spermwhaleipi/spermwhaleipi_v1_tes1_uidlist.pgdf", json_path="spermwhaleipi_v1_test1_uidlist.json", filters=Filters({'uidlist': WhitelistFilter([2000002])}))

    # click_v4_test2 = load_pamguard_binary_file("../tests/dataset/detectors/click/click_v4_test2.pgdf", json_path="click_v4_test2.json")
    # click_v4_test2_daterange = load_pamguard_binary_file("../tests/dataset/detectors/click/click_v4_test2.pgdf", json_path="click_v4_test2_daterange.json", filters=Filters({'daterange': DateFilter(datetime.datetime.fromtimestamp(1751975573249 / 1000, tz = datetime.UTC), datetime.datetime.fromtimestamp(1751975698249 / 1000, tz = datetime.UTC), ordered=True)}))
    # click_v4_test2_uidlist = load_pamguard_binary_file("../tests/dataset/detectors/click/click_v4_test2.pgdf", json_path="click_v4_test2_uidlist.json", filters=Filters({'uidlist': WhitelistFilter([2000002])}))

    # click_v4_test3 = load_pamguard_binary_file("../tests/dataset/detectors/click/click_v4_test3.pgdf", json_path="click_v4_test3.json")
    # click_v4_test3_daterange = load_pamguard_binary_file("../tests/dataset/detectors/click/click_v4_test3.pgdf", json_path="click_v4_test3_daterange.json", filters=Filters({'daterange': DateFilter(datetime.datetime.fromtimestamp(1751975573249 / 1000, tz = datetime.UTC), datetime.datetime.fromtimestamp(1751975698249 / 1000, tz = datetime.UTC), ordered=True)}))
    # click_v4_test3_uidlist = load_pamguard_binary_file("../tests/dataset/detectors/click/click_v4_test3.pgdf", json_path="click_v4_test3_uidlist.json", filters=Filters({'uidlist': WhitelistFilter([2000002])}))

    # noisemonitor_v2_test1 = load_pamguard_binary_file("../tests/dataset/processing/noisemonitor/noisemonitor_v2_test1.pgdf", json_path="noisemonitor_v2_test1.json")
    # noisemonitor_v2_test1_daterange = load_pamguard_binary_file("../tests/dataset/processing/noisemonitor/noisemonitor_v2_test1.pgdf", json_path="noisemonitor_v2_test1_daterange.json", filters=Filters({'daterange': DateFilter(datetime.datetime.fromtimestamp(1499572713281 / 1000, tz = datetime.UTC), datetime.datetime.fromtimestamp(1499572713291 / 1000, tz = datetime.UTC), ordered=True)}))
    # noisemonitor_v2_test1_uidlist = load_pamguard_binary_file("../tests/dataset/processing/noisemonitor/noisemonitor_v2_test1.pgdf", json_path="noisemonitor_v2_test1_uidlist.json", filters=Filters({'uidlist': WhitelistFilter([1000005])}))

    # noiseband_v3_test1_daterange = load_pamguard_binary_file("../tests/dataset/processing/noiseband/noiseband_v3_test1.pgdf", json_path="noiseband_v3_test1_daterange.json", filters=Filters({'daterange': DateFilter(datetime.datetime.fromtimestamp(1499572333281 / 1000, tz = datetime.UTC), datetime.datetime.fromtimestamp(1533053591103 / 1000, tz = datetime.UTC), ordered=True)}))

    # noisebandnoise_v3_test1 = load_pamguard_binary_file("../tests/dataset/processing/noiseband/noisebandnoise_v3_test1.pgdf", json_path="noisebandnoise_v3_test1.json")
    # noisebandnoise_v3_test1_daterange = load_pamguard_binary_file("../tests/dataset/processing/noiseband/noisebandnoise_v3_test1.pgdf", json_path="noisebandnoise_v3_test1_daterange.json", filters=Filters({'daterange': DateFilter(datetime.datetime.fromtimestamp(1499572713281 / 1000, tz = datetime.UTC), datetime.datetime.fromtimestamp(1499572713291 / 1000, tz = datetime.UTC), ordered=True)}))
    # noisebandnoise_v3_test1_uidlist = load_pamguard_binary_file("../tests/dataset/processing/noiseband/noisebandnoise_v3_test1.pgdf", json_path="noisebandnoise_v3_test1_uidlist.json", filters=Filters({'uidlist': WhitelistFilter([1000005])}))

    # noisebandpulses_v3_test1 = load_pamguard_binary_file("../tests/dataset/processing/noiseband/noisebandpulses_v3_test1.pgdf", json_path="noisebandpulses_v3_test1.json")
    # noisebandpulses_v3_test1_daterange = load_pamguard_binary_file("../tests/dataset/processing/noiseband/noisebandpulses_v3_test1.pgdf", json_path="noisebandpulses_v3_test1_daterange.json", filters=Filters({'daterange': DateFilter(datetime.datetime.fromtimestamp(1499572713281 / 1000, tz = datetime.UTC), datetime.datetime.fromtimestamp(1499572713291 / 1000, tz = datetime.UTC), ordered=True)}))
    # noisebandpulses_v3_test1_uidlist = load_pamguard_binary_file("../tests/dataset/processing/noiseband/noisebandpulses_v3_test1.pgdf", json_path="noisebandpulses_v3_test1_uidlist.json", filters=Filters({'uidlist': WhitelistFilter([1000005])}))

    # clipgenerator_v3_test1 = load_pamguard_binary_file("../tests/dataset/processing/clipgenerator/clipgenerator_v3_test1.pgdf", json_path="clipgenerator_v3_test1.json")
    # clipgenerator_v3_test1_daterange = load_pamguard_binary_file("../tests/dataset/processing/clipgenerator/clipgenerator_v3_test1.pgdf", json_path="clipgenerator_v3_test1_daterange.json")
    # clipgenerator_v3_test1_uidlist = load_pamguard_binary_file("../tests/dataset/processing/clipgenerator/clipgenerator_v3_test1.pgdf", json_path="clipgenerator_v3_test1_uidlist.json")

    # clipgenerator_v3_test2 = load_pamguard_binary_file("../tests/dataset/processing/clipgenerator/clipgenerator_v3_test2.pgdf", json_path="clipgenerator_v3_test2.json")
    # clipgenerator_v3_test2_daterange = load_pamguard_binary_file("../tests/dataset/processing/clipgenerator/clipgenerator_v3_test2.pgdf", json_path="clipgenerator_v3_test2_daterange.json")
    # clipgenerator_v3_test2_uidlist = load_pamguard_binary_file("../tests/dataset/processing/clipgenerator/clipgenerator_v3_test2.pgdf", json_path="clipgenerator_v3_test2_uidlist.json")

    # dbht_v2_test1 = load_pamguard_binary_file("../tests/dataset/processing/dbht/dbht_v2_test1.pgdf", json_path="dbht_v2_test1.json")
    # dbht_v2_test1_daterange = load_pamguard_binary_file("../tests/dataset/processing/dbht/dbht_v2_test1.pgdf", json_path="dbht_v2_test1_daterange.json", filters=Filters({'daterange': DateFilter(datetime.datetime.fromtimestamp(1751974755492 / 1000, tz = datetime.UTC), datetime.datetime.fromtimestamp(1751974792491 / 1000, tz = datetime.UTC), ordered=True)}))
    # dbht_v2_test1_uidlist = load_pamguard_binary_file("../tests/dataset/processing/dbht/dbht_v2_test1.pgdf", json_path="dbht_v2_test1_uidlist.json", filters=Filters({'uidlist': WhitelistFilter([4000161])}))

    # difar_v2_test1 = load_pamguard_binary_file("../tests/dataset/processing/difar/difar_v2_test1.pgdf", json_path="difar_v2_test1.json")
    # difar_v2_test1_daterange = load_pamguard_binary_file("../tests/dataset/processing/difar/difar_v2_test1.pgdf", json_path="difar_v2_test1_daterange.json", filters=Filters({'daterange': DateFilter(datetime.datetime.fromtimestamp(1533049096511 / 1000, tz = datetime.UTC), datetime.datetime.fromtimestamp(1533049175551 / 1000, tz = datetime.UTC), ordered=True)}))
    # difar_v2_test1_uidlist = load_pamguard_binary_file("../tests/dataset/processing/difar/difar_v2_test1.pgdf", json_path="difar_v2_test1_uidlist.json", filters=Filters({'uidlist': WhitelistFilter([2])}))

    # difar_v2_test2 = load_pamguard_binary_file("../tests/dataset/processing/difar/difar_v2_test2.pgdf", verbosity=Verbosity.ERROR)
    # print(difar_v2_test2.data[19])
    #print(difar_v2_test2.file_header)
    #print(difar_v2_test2.module_header)
    
    # for i, d in enumerate(difar_v2_test2.data):
    #     if d.channel_map == None:
    #         print(i, d)
    # difar_v2_test2 = load_pamguard_binary_file("../tests/dataset/processing/difar/difar_v2_test2.pgdf", json_path="difar_v2_test2.json")
    # difar_v2_test2_daterange = load_pamguard_binary_file("../tests/dataset/processing/difar/difar_v2_test2.pgdf", json_path="difar_v2_test2_daterange.json", filters=Filters({'daterange': DateFilter(datetime.datetime.fromtimestamp(1533049238271 / 1000, tz = datetime.UTC), datetime.datetime.fromtimestamp(1533049697599 / 1000, tz = datetime.UTC), ordered=True)}))
    # difar_v2_test2_uidlist = load_pamguard_binary_file("../tests/dataset/processing/difar/difar_v2_test2.pgdf", json_path="difar_v2_test2_uidlist.json", filters=Filters({'uidlist': WhitelistFilter([2,3,4,5,6,7,8,10])}))

    # difar_v2_test3 = load_pamguard_binary_file("../tests/dataset/processing/difar/difar_v2_test3.pgdf", json_path="difar_v2_test3.json")
    # difar_v2_test3_daterange = load_pamguard_binary_file("../tests/dataset/processing/difar/difar_v2_test3.pgdf", json_path="difar_v2_test3_daterange.json", filters=Filters({'daterange': DateFilter(datetime.datetime.fromtimestamp(1533052916351 / 1000, tz = datetime.UTC), datetime.datetime.fromtimestamp(1533053591103 / 1000, tz = datetime.UTC), ordered=True)}))
    # difar_v2_test3_uidlist = load_pamguard_binary_file("../tests/dataset/processing/difar/difar_v2_test3.pgdf", json_path="difar_v2_test3_uidlist.json", filters=Filters({'uidlist': WhitelistFilter([178])}))

    # ishmaeldetections_energysum_v2_test1 = load_pamguard_binary_file("../tests/dataset/processing/ishmael/ishmaeldetections_energysum_v2_test1.pgdf", json_path="ishmaeldetections_energysum_v2_test1.json")
    # ishmaeldetections_energysum_v2_test2 = load_pamguard_binary_file("../tests/dataset/processing/ishmael/ishmaeldetections_energysum_v2_test2.pgdf", json_path="ishmaeldetections_energysum_v2_test2.json")
    # ishmaeldetections_energysum_v2_test3 = load_pamguard_binary_file("../tests/dataset/processing/ishmael/ishmaeldetections_energysum_v2_test3.pgdf", json_path="ishmaeldetections_energysum_v2_test3.json")

    # ishmaeldetections_matchedfilter_v2_test1 = load_pamguard_binary_file("../tests/dataset/processing/ishmael/ishmaeldetections_matchedfilter_v2_test1.pgdf", json_path="ishmaeldetections_matchedfilter_v2_test1.json")
    # ishmaeldetections_matchedfilter_v2_test2 = load_pamguard_binary_file("../tests/dataset/processing/ishmael/ishmaeldetections_matchedfilter_v2_test2.pgdf", json_path="ishmaeldetections_matchedfilter_v2_test2.json")

    # ishmaeldetections_spectrogramcorrelation_v2_test1 = load_pamguard_binary_file("../tests/dataset/processing/ishmael/ishmaeldetections_spectrogramcorrelation_v2_test1.pgdf", json_path="ishmaeldetections_spectrogramcorrelation_v2_test1.json")
    # ishmaeldetections_spectrogramcorrelation_v2_test2 = load_pamguard_binary_file("../tests/dataset/processing/ishmael/ishmaeldetections_spectrogramcorrelation_v2_test2.pgdf", json_path="ishmaeldetections_spectrogramcorrelation_v2_test2.json")

    # ais_test1 = load_pamguard_binary_file("../tests/dataset/ais/AIS_Processing_AIS_Processing_AIS_Processing_20250714_154433.pgdf", json_path="ais_test1.json")

    # gpl_v2_test1 = load_pamguard_binary_file("../tests/dataset/detectors/gpl/gpl_v2_test1.pgdf", json_path="gpl_v2_test1.json")
    # gpl_v2_test1_background = load_pamguard_binary_file("../tests/dataset/detectors/gpl/gpl_v2_test1.pgnf", json_path="gpl_v2_test1_background.json")

    # gpl_v2_test2 = load_pamguard_binary_file("../tests/dataset/detectors/gpl/gpl_v2_test2.pgdf", json_path="gpl_v2_test2.json")
    # gpl_v2_test2_background = load_pamguard_binary_file("../tests/dataset/detectors/gpl/gpl_v2_test2.pgnf", json_path="gpl_v2_test2_background.json")

    # geminithreshold_test1 = load_pamguard_binary_file("../tests/dataset/plugins/geminithreshold/Gemini_Threshold_Detector_Filtered_Threshold_Detector_Sonar_Tracks_20241015_050000.pgdf", json_path="geminithreshold_test1.json")
    # geminithreshold_test1_background = load_pamguard_binary_file("../tests/dataset/plugins/geminithreshold/Gemini_Threshold_Detector_Filtered_Threshold_Detector_Sonar_Tracks_20241015_050000.pgnf", json_path="geminithreshold_test1_background.json")

    # whistleandmoan_v2_test1_background = load_pamguard_binary_file("../tests/dataset/detectors/whistleandmoan/whistleandmoan_v2_test1.pgnf", json_path="whistleandmoan_v2_test1_background.json")

    # click_v4_test1 = load_pamguard_binary_file("../tests/dataset/detectors/click/click_v4_test1.pgdf", json_path="click_v4_test1.json")
    # click_v4_test1_background = load_pamguard_binary_file("../tests/dataset/detectors/click/click_v4_test1.pgnf", json_path="click_v4_test1_background.json")
    
    # click_v4_test2 = load_pamguard_binary_file("../tests/dataset/detectors/click/click_v4_test2.pgdf", json_path="click_v4_test2.json")
    # click_v4_test2_background = load_pamguard_binary_file("../tests/dataset/detectors/click/click_v4_test2.pgnf", json_path="click_v4_test2_background.json")
    
    # click_v4_test3 = load_pamguard_binary_file("../tests/dataset/detectors/click/click_v4_test3.pgdf", json_path="click_v4_test3.json")
    # click_v4_test3_background = load_pamguard_binary_file("../tests/dataset/detectors/click/click_v4_test3.pgnf", json_path="click_v4_test3_background.json")

    # deeplearningclassifier_v2_test1_detections = load_pamguard_binary_file("../tests/dataset/classifiers/deeplearningclassifier/deeplearningclassifier_v2_test1_detections.pgdf", json_path="deeplearningclassifier_v2_test1_detections.json")
    # deeplearningclassifier_v2_test1_models = load_pamguard_binary_file("../tests/dataset/classifiers/deeplearningclassifier/deeplearningclassifier_v2_test1_models.pgdf", json_path="deeplearningclassifier_v2_test1_models.json")
    # deeplearningclassifier_v2_test1_models = load_pamguard_binary_file("../tests/dataset/classifiers/deeplearningclassifier/deeplearningclassifier_v2_test1_models.pgdf")

    deeplearningclassifier_v2_test1_models = load_pamguard_binary_file("../tests/dataset/classifiers/deeplearningclassifier/deeplearningclassifier_v2_test1_models.pgdx", verbosity=Verbosity.ERROR)
    print(deeplearningclassifier_v2_test1_models.file_header)

    print()
    deeplearningclassifier_v2_test1_models = load_pamguard_binary_file("../tests/dataset/classifiers/deeplearningclassifier/deeplearningclassifier_v2_test1_models.pgdf", verbosity=Verbosity.ERROR)
    print(deeplearningclassifier_v2_test1_models.file_header)



    # difar_v2_test3_daterange = load_pamguard_binary_file("../tests/dataset/processing/difar/difar_v2_test2.pgdf",verbosity=Verbosity.DEBUG)
    # from .load_pamguard_binary_folder import load_pamguard_binary_folder
    # ods = load_pamguard_binary_folder("../tests/dataset/detectors/gpl", "gpl*.pgdf")
    # print(ods)

    # cd = load_pamguard_binary_file("../tests/dataset/detectors/click/click_v4_test1.pgdx", json_path="cd.json", verbosity=Verbosity.DEBUG)
    # print(cd.data)
    # print(cd.to_json())