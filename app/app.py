from cmath import nan
import re
from flask import Flask, render_template, request, send_file, after_this_request
from datetime import datetime
import os
from lxml import etree as et
import glob
from io import BytesIO
from zipfile import ZipFile
import pandas as pd
# import pysftp
import paramiko
import pysftp
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/bulk')
def bulk():
    return render_template('bulk.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':

        # MANIFEST GENERATOR 
        root = et.Element("CargoManifest")

        # MessageHeader Data 
        MessageHeader = et.SubElement(root, 'MessageHeader')

        MessageSender = et.SubElement(MessageHeader, 'MessageSender')
        customs_code = et.SubElement(MessageSender, 'customs_code')
        customs_code.text = 'L2600'
        user_id = et.SubElement(MessageSender, 'user_id')
        user_id.text = '147504122018000'

        MessageDate = et.SubElement(MessageHeader, 'MessageDate')
        MessageDate.text = datetime.today().strftime('%d%m%Y')
        MessageTime = et.SubElement(MessageHeader, 'MessageTime')
        MessageTime.text = datetime.today().strftime('%H%M')
        CourierManifest = et.SubElement(MessageHeader, 'CourierManifest')
        CourierManifest.text = 'Y'
        GlobalGuaranteePayment = et.SubElement(MessageHeader, 'GlobalGuaranteePayment')
        GlobalGuaranteePayment.text = 'Y'

        # ManifestRecord Data 
        ManifestRecord = et.SubElement(root, 'ManifestRecord')

        # ManifestHeader Data 
        ManifestHeader = et.SubElement(ManifestRecord, 'ManifestHeader')
        ManifestNo = et.SubElement(ManifestHeader, 'ManifestNo')
        ManifestNo.text = request.form['ManifestNo']
        TransportMode = et.SubElement(ManifestHeader, 'TransportMode')
        TransportMode.text = request.form['TransportMode']
        # GeneralManifestNo = et.SubElement(ManifestHeader, 'GeneralManifestNo')
        # GeneralManifestNo.text = ''
        TransportDocType = et.SubElement(ManifestHeader, 'TransportDocType')
        TransportDocType.text = 'IN'

        PortOfDischarge = et.SubElement(ManifestHeader, 'PortOfDischarge')
        CountryCode = et.SubElement(PortOfDischarge, 'CountryCode')
        CountryCode.text = request.form['PortOfDischargeCountryCode']
        PortCode = et.SubElement(PortOfDischarge, 'PortCode')
        PortCode.text = request.form['PortOfDischargePortCode']
        PortName = et.SubElement(PortOfDischarge, 'PortName')
        PortName.text = request.form['PortOfDischargePortName']
        PortType = et.SubElement(PortOfDischarge, 'PortType')
        PortType.text = 'A'

        NumberofTrnDocs = et.SubElement(ManifestHeader, 'NumberofTrnDocs')
        NumberofTrnDocs.text = request.form['NumberofTrnDocs']

        # MeansOfTransport Data 
        MeansOfTransport = et.SubElement(ManifestRecord, 'MeansOfTransport')
        MeansofTransportNumber = et.SubElement(MeansOfTransport, 'MeansofTransportNumber')
        MeansofTransportNumber.text = request.form['MeansofTransportNumber']
        MeansofTransportName = et.SubElement(MeansOfTransport, 'MeansofTransportName')
        MeansofTransportName.text = request.form['MeansofTransportName']
        MeansofTransportNat = et.SubElement(MeansOfTransport, 'MeansofTransportNat')
        MeansofTransportNat.text = request.form['MeansofTransportNat']
        FlightVoyageNumber = et.SubElement(MeansOfTransport, 'FlightVoyageNumber')
        FlightVoyageNumber.text = request.form['FlightVoyageNumber']
        ETA = et.SubElement(MeansOfTransport, 'ETA')
        ETA.text = request.form['MeansofTransportETADate']
        ETD = et.SubElement(MeansOfTransport, 'ETD')
        ETD.text = request.form['MeansofTransportETDDate']

        # TransportDocumentList Data 
        TransportDocumentList = et.SubElement(ManifestRecord, 'TransportDocumentList')

        TransportDocument = et.SubElement(TransportDocumentList, 'TransportDocument')
        TransportDocNumber = et.SubElement(TransportDocument, 'TransportDocNumber')
        TransportDocNumber.text = request.form['TransportDocNumber']
        TotalQuantity = et.SubElement(TransportDocument, 'TotalQuantity')
        Quantity = et.SubElement(TotalQuantity, 'Quantity')
        Quantity.text = request.form['TDTotalQuantity']
        UOM = et.SubElement(TotalQuantity, 'UOM')
        UOM.text = 'CTN'
        TotalGrossWeight = et.SubElement(TransportDocument, 'TotalGrossWeight')
        Quantity  = et.SubElement(TotalGrossWeight, 'Quantity')
        Quantity.text = request.form['TDTotalGrossWeight']
        UOM = et.SubElement(TotalGrossWeight, 'UOM')
        UOM.text = 'KG'
        # PortofLoading = et.SubElement(TransportDocument, 'PortofLoading')
        # CountryCode = et.SubElement(PortofLoading, 'CountryCode')
        # PortCode = et.SubElement(PortofLoading, 'PortCode')
        # PortName = et.SubElement(PortofLoading, 'PortName')
        # PortType = et.SubElement(PortofLoading, 'PortType')
        FirstPortofLoading = et.SubElement(TransportDocument, 'FirstPortofLoading')
        CountryCode = et.SubElement(FirstPortofLoading, 'CountryCode')
        CountryCode.text = request.form['FirstPortofLoadingCountryCode']
        PortCode = et.SubElement(FirstPortofLoading, 'PortCode')
        PortCode.text = request.form['FirstPoLPortCode']
        PortName = et.SubElement(FirstPortofLoading, 'PortName')
        PortName.text = request.form['FirstPortofLoadingPortName']
        PortType = et.SubElement(FirstPortofLoading, 'PortType')
        PortType.text = 'A'
        # PortofDischarge = et.SubElement(TransportDocument, 'PortofDischarge')
        # CountryCode = et.SubElement(PortOfDischarge, 'CountryCode')
        # CountryCode.text = request.form['PortOfDischargeCountryCode']
        # PortCode = et.SubElement(PortOfDischarge, 'PortCode')
        # PortCode.text = request.form['PortOfDischargePortCode']
        # PortName = et.SubElement(PortOfDischarge, 'PortName')
        # PortName.text = request.form['PortOfDischargePortName']
        # PortType = et.SubElement(PortOfDischarge, 'PortType')
        # PortType.text = 'A'

        FinalDestination  = et.SubElement(TransportDocument, 'FinalDestination')
        FinalDestination.text ='QA'

        PartyList = et.SubElement(TransportDocument, 'PartyList')
        # Party = et.SubElement(PartyList, 'Party')
        # PartyType = et.SubElement(Party, 'PartyType')
        # PartyName = et.SubElement(Party, 'PartyName')
        # PartyAddress = et.SubElement(Party, 'PartyAddress')
        
        ContainerList = et.SubElement(TransportDocument, 'ContainerList')
        # Container = et.SubElement(ContainerList, 'Container')
        # ContainerNumber = et.SubElement(Container, 'ContainerNumber')
        # ContainerType = et.SubElement(Container, 'ContainerType')
        # ContainerSize = et.SubElement(Container, 'ContainerSize')

        ItemList = et.SubElement(TransportDocument, 'ItemList')
        Item = et.SubElement(ItemList, 'Item')
        ItemDescription = et.SubElement(Item, 'ItemDescription')
        ItemDescription.text = request.form['ItemDescription']
        ItemCOO = et.SubElement(Item, 'ItemCOO')
        ItemCOO.text = request.form['ItemCOO']
        ItemQuantity = et.SubElement(Item, 'ItemQuantity')
        Quantity = et.SubElement(ItemQuantity, 'Quantity')
        Quantity.text = request.form['ItemQuantity']
        UOM = et.SubElement(ItemQuantity, 'UOM')
        UOM.text = 'PCS'
        ItemGrossWeight = et.SubElement(Item, 'ItemGrossWeight')
        Quantity = et.SubElement(ItemGrossWeight, 'Quantity')
        Quantity.text = request.form['ItemGrossWeight']
        UOM = et.SubElement(ItemGrossWeight, 'UOM')
        UOM.text = 'KG'
        ItemPackagingType = et.SubElement(Item, 'ItemPackagingType')
        ItemMarksNumbers = et.SubElement(Item, 'ItemMarksNumbers')
        ItemMarksNumbers.text = request.form['TransportDocNumber']
        # Master Airway Number
        ItemDGFlag = et.SubElement(Item, 'ItemDGFlag')
        ItemDGFlag.text = 'N'


        RouteList = et.SubElement(TransportDocument, 'RouteList')
        # Route = et.SubElement(RouteList, 'Route')
        # Port = et.SubElement(Route, 'Port')
        # CountryCode = et.SubElement(Port, 'CountryCode')
        # PortCode = et.SubElement(Port, 'PortCode')
        # PortName = et.SubElement(Port, 'PortName')
        # PortType = et.SubElement(Port, 'PortType')


        # DocList  = et.SubElement(TransportDocument, 'DocList')
        # DocAttachment = et.SubElement(DocList, 'DocAttachment')
        # Title = et.SubElement(DocAttachment, 'Title')
        # FileName = et.SubElement(DocAttachment, 'FileName')

        tree = et.ElementTree(root)
        et.indent(tree, space="\t", level=0)
        tree.write('form-manifest.xml', encoding="utf-8")


        # DECLARATION GENERATOR 
        xmlns = "/schema/declaration"
        xsi = "http://www.w3.org/2001/XMLSchema-instance"
        schemaLocation = "/schema/declaration_schema.xsd"
        
        root = et.Element(
            "{" + xmlns + "}CustomsDeclaration",
            attrib={"{" + xsi + "}schemaLocation": schemaLocation},
            nsmap={'xsi': xsi, None: xmlns}
        )

        # MessageHeader Data 
        MessageHeader = et.SubElement(root, 'MessageHeader')

        docType = et.SubElement(MessageHeader, 'docType')
        batchID = et.SubElement(MessageHeader, 'batchID')
        MessageSender = et.SubElement(MessageHeader, 'MessageSender')
        UserId = et.SubElement(MessageSender, 'UserId')
        MessageDate = et.SubElement(MessageHeader, 'MessageDate')
        MessageTime = et.SubElement(MessageHeader, 'MessageTime')

        docType.text = 'CUSDEC'
        batchID.text = 'qccsw1'
        UserId.text = '147504122018000'
        MessageDate.text = datetime.today().strftime('%d%m%Y')
        MessageTime.text = datetime.today().strftime('%H%M')

        DeclarationRecord = et.SubElement(root, 'DeclarationRecord')
        Payload = et.SubElement(DeclarationRecord, 'Payload')
        Action = et.SubElement(Payload, 'Action')
        Action.text = 'Submit'

        # DeclarationHeader Data 
        DeclarationHeader = et.SubElement(Payload, 'DeclarationHeader')

        DeclarationType = et.SubElement(DeclarationHeader, 'DeclarationType')
        StatisticalDecFlag = et.SubElement(DeclarationHeader, 'StatisticalDecFlag')
        OnsiteInspectionFlag = et.SubElement(DeclarationHeader, 'OnsiteInspectionFlag')
        ContainerTransportIndicator = et.SubElement(DeclarationHeader, 'ContainerTransportIndicator')
        StrategicGoods = et.SubElement(DeclarationHeader, 'StrategicGoods')
        Remarks = et.SubElement(DeclarationHeader, 'Remarks')
        CourierDeclaration = et.SubElement(DeclarationHeader, 'CourierDeclaration')
        ExpressCompanies = et.SubElement(DeclarationHeader, 'ExpressCompanies')
        ModeofPayment = et.SubElement(DeclarationHeader, 'ModeofPayment')
        GuaranteeAccount = et.SubElement(DeclarationHeader, 'GuaranteeAccount')

        DeclarationType.text = 'IMP'
        StatisticalDecFlag.text = 'N'
        OnsiteInspectionFlag.text = 'N'
        ContainerTransportIndicator.text = 'N'
        StrategicGoods.text = 'N'
        Remarks.text = ''
        CourierDeclaration.text = 'Y'
        ExpressCompanies.text = '130453'
        ModeofPayment.text = 'G'
        GuaranteeAccount.text = 'C'

        # Party Data 
        Party = et.SubElement(Payload, 'Party')

        Importer = et.SubElement(Party, 'Importer')
        ImporterCode  = et.SubElement(Importer, 'ImporterCode')
        ImporterName = et.SubElement(Importer, 'ImporterName')
        ImporterAddress = et.SubElement(Importer, 'ImporterAddress')
        ImporterPhone = et.SubElement(Importer, 'ImporterPhone')
        ImporterIdType = et.SubElement(Importer, 'ImporterIdType')
        ImporterIdNo = et.SubElement(Importer, 'ImporterIdNo')

        ImporterCode.text = ''
        ImporterName.text = request.form['ReceiverName']
        ImporterAddress.text = request.form['ReceiverAddress']
        ImporterPhone.text = request.form['ReceiverPhone']
        ImporterIdType.text = request.form['ImporterIdType']
        ImporterIdNo.text = request.form['ImporterIdNo']

        Exporter = et.SubElement(Party, 'Exporter')
        ExporterCode = et.SubElement(Exporter, 'ExporterCode')
        ExporterName = et.SubElement(Exporter, 'ExporterName')
        ExporterAddress = et.SubElement(Exporter, 'ExporterAddress')
        ExporterPhoneNo = et.SubElement(Exporter, 'ExporterPhoneNo')

        ExporterCode.text = ''
        ExporterName.text = request.form['SenderName']
        ExporterAddress.text = request.form['SenderAddress']
        ExporterPhoneNo.text = request.form['SenderPhone']

        # BoL Data 
        BillOfLading = et.SubElement(Payload, 'BillOfLading')
        CargoManifestNumber = et.SubElement(BillOfLading, 'CargoManifestNumber')
        CargoManifestNumber.text = request.form['CargoManifestNumber']
        MasterBLNumber = et.SubElement(BillOfLading, 'MasterBLNumber')
        MasterBLNumber.text = request.form['MasterBLNumber']
        HouseBLNumber = et.SubElement(BillOfLading, 'HouseBLNumber')
        HouseBLNumber.text = request.form['TransportDocNumber']
        PortOfLoading = et.SubElement(BillOfLading, 'PortOfLoading')
        PortOfLoading.text = request.form['BoLPortOfLoading']
        DateofArrivalOrDeparture = et.SubElement(BillOfLading, 'DateofArrivalOrDeparture')
        DateofArrivalOrDeparture.text = request.form['DateofArrivalOrDeparture']
        FinalDestination = et.SubElement(BillOfLading, 'FinalDestination')
        FinalDestination.text ='QA'
        TransportMeans = et.SubElement(BillOfLading, 'TransportMeans')
        Identification = et.SubElement(TransportMeans, 'Identification')
        Identification.text = request.form['TransportIdentification']
        Name = et.SubElement(TransportMeans, 'Name')
        Name.text = request.form['TransportName']
        Nationality = et.SubElement(TransportMeans, 'Nationality')
        Nationality.text = request.form['TransportNationality']
        VoyageNumber = et.SubElement(TransportMeans, 'VoyageNumber')
        VoyageNumber.text = request.form['TransportVoyageNumber']
        BLNumberOfPackages = et.SubElement(BillOfLading, 'BLNumberOfPackages')
        NumberOfPackages = et.SubElement(BLNumberOfPackages, 'BLNumberOfPackages')
        NumberOfPackages.text = request.form['NumberOfPackagesBL']
        UOM = et.SubElement(BLNumberOfPackages, 'UOM')
        UOM.text = 'PCS'
        BLGrossWeight = et.SubElement(BillOfLading, 'BLGrossWeight')
        Weight = et.SubElement(BLGrossWeight, 'UOM')
        Weight.text = request.form['BLGrossWeight']
        UOM = et.SubElement(BLGrossWeight, 'UOM')
        UOM.text = 'KG'


        
        # Containers Data 
        Containers = et.SubElement(Payload, 'Containers')

        Container = et.SubElement(Containers, 'Container')
        ContainerNumber = et.SubElement(Container, 'ContainerNumber')
        ContainerType = et.SubElement(Container, 'ContainerType')
        ContainerWeight = et.SubElement(Container, 'ContainerWeight')
        Weight = et.SubElement(ContainerWeight, 'Weight')
        UOM = et.SubElement(ContainerWeight, 'UOM')
        Weight.text = '1'
        UOM.text = 'A'
        TareWeight = et.SubElement(Container, 'TareWeight')
        Weight = et.SubElement(TareWeight, 'Weight')
        UOM = et.SubElement(TareWeight, 'UOM')
        Weight.text = '1'
        UOM.text = 'A'

        ContainerNumber.text = ''
        ContainerType.text = ''

        # Seals Data 
        Seals = et.SubElement(Payload, 'Seals')
        Seal = et.SubElement(Seals, 'Seal')
        
        SealNumber = et.SubElement(Seal, 'SealNumber')
        SealNumber.text = ' '
        CountryCode = et.SubElement(Seal, 'CountryCode')
        CountryCode.text = 'QA'
        ContainerNumber = et.SubElement(Seal, 'ContainerNumber')


        CertificateOfOrigins = et.SubElement(Payload, 'CertificateOfOrigins')
        Invoices = et.SubElement(Payload, 'Invoices')
        CertificateOfOrigins.text = ''
        Invoices.text = ''

        # Item Data
        Items = et.SubElement(Payload, 'Items')
        LineItem = et.SubElement(Items, 'LineItem')

        TariffCodeNumber = et.SubElement(LineItem, 'TariffCodeNumber')
        TariffCodeNumber.text = 'ASDFGHJK'
        ItemDescriptionAdditional = et.SubElement(LineItem, 'ItemDescriptionAdditional')
        ItemDescriptionAdditional.text = ' '
        CountryofOriginCoded = et.SubElement(LineItem, 'CountryofOriginCoded')
        CountryofOriginCoded.text = 'KW'

        VehicleDetails = et.SubElement(LineItem, 'VehicleDetails')
        ChassisNumber = et.SubElement(VehicleDetails, 'ChassisNumber')
        VehicleMake = et.SubElement(VehicleDetails, 'VehicleMake')
        VehicleModel = et.SubElement(VehicleDetails, 'VehicleModel')
        VehicleCategory = et.SubElement(VehicleDetails, 'VehicleCategory')
        ModelYear = et.SubElement(VehicleDetails, 'ModelYear')
        Color = et.SubElement(VehicleDetails, 'Color')
        EngineNumber = et.SubElement(VehicleDetails, 'EngineNumber')
        EngineCapacity = et.SubElement(VehicleDetails, 'EngineCapacity')
        ManufacturingDate = et.SubElement(VehicleDetails, 'ManufacturingDate')
        VehicleCondition = et.SubElement(VehicleDetails, 'VehicleCondition')
        NumberOfCylinders = et.SubElement(VehicleDetails, 'NumberOfCylinders')

        ChassisNumber.text = 'string'
        VehicleMake.text = 'string'
        VehicleModel.text = 'string'
        VehicleCategory.text = 'stonk'
        ModelYear.text = '1997'
        Color.text = 'string'
        EngineNumber.text = 'string'
        EngineCapacity.text = 'string'
        ManufacturingDate.text = '1995-09-10'
        VehicleCondition.text = 'NEW'
        NumberOfCylinders.text = '42'

        AdditionalInformation = et.SubElement(LineItem, 'AdditionalInformation')
        
        ItemGrossWeight = et.SubElement(LineItem, 'ItemGrossWeight')
        Weight = et.SubElement(ItemGrossWeight, 'Weight')
        UOM = et.SubElement(ItemGrossWeight, 'UOM')
        Weight.text = '2902800.2349058'
        UOM.text = 'KG'


        ItemNetWeight = et.SubElement(LineItem, 'ItemNetWeight')
        Weight = et.SubElement(ItemNetWeight, 'Weight')
        UOM = et.SubElement(ItemNetWeight, 'UOM')
        Weight.text = '7534120.2349058'
        UOM.text = 'KG'

        ItemQuantity = et.SubElement(LineItem, 'ItemQuantity')
        Quantity = et.SubElement(ItemQuantity, 'Quantity')
        UOM = et.SubElement(ItemQuantity, 'UOM')
        Quantity.text = '49020.2349058039'
        UOM.text = 'A'

        FreeOfCostQuantity = et.SubElement(LineItem, 'FreeOfCostQuantity')
        Quantity = et.SubElement(FreeOfCostQuantity, 'Quantity')
        Quantity.text = '2080000.2349058'

        Shortage = et.SubElement(LineItem, 'Shortage')
        Shortage.text = 'N'

        ShortageQuantity = et.SubElement(LineItem, 'ShortageQuantity')
        ShortageQuantity.text = '2477340.2349058'

        RefDeclarationNumber = et.SubElement(LineItem, 'RefDeclarationNumber')
        RefDeclarationNumber.text = 'string'

        ItemValue = et.SubElement(LineItem, 'ItemValue')
        CargoType = et.SubElement(LineItem, 'CargoType')
        CargoType.text = 'OTH'
        
        tree = et.ElementTree(root)
        et.indent(tree, space="\t", level=0)
        tree.write('form-declaration.xml', encoding="utf-8")

        target = '/app/'

        stream = BytesIO()
        with ZipFile(stream, 'w') as zf:
            for file in glob.glob(os.path.join(target, '*.xml')):
                zf.write(file, os.path.basename(file))
        stream.seek(0)

        for xml in glob.glob(os.path.join(target, '*.xml')):
            os.remove(xml)

        return send_file(
            stream,
            as_attachment=True,
            attachment_filename='Form-XMLs.zip'
        )

    else:
        return render_template('form.html')

@app.route('/bulkmanifest', methods=['GET', 'POST'])
def bulkmanifest():
    if request.method == 'POST':
        @after_this_request
        def delete_xml(response):
            target = '/app/'
            filelist = glob.glob(os.path.join(target, "*.xml"))
            for f in filelist:
                os.remove(f)
            return response

        f = f = request.files['manifestxlsfile']
        raw_data = pd.read_excel(f)
        
        root = et.Element("CargoManifest")
        
        # MessageHeader Data 
        MessageHeader = et.SubElement(root, 'MessageHeader')
        MessageSender = et.SubElement(MessageHeader, 'MessageSender')
        customs_code = et.SubElement(MessageSender, 'customs_code')
        customs_code.text = 'L2600'
        user_id = et.SubElement(MessageSender, 'user_id')
        user_id.text = '147504122018000'

        MessageDate = et.SubElement(MessageHeader, 'MessageDate')
        MessageTime = et.SubElement(MessageHeader, 'MessageTime')
        MessageDate.text = datetime.today().strftime('%d%m%Y')
        MessageTime.text = datetime.today().strftime('%H%M')
        CourierManifest = et.SubElement(MessageHeader, 'CourierManifest')
        CourierManifest.text = 'Y'
        # GlobalGuaranteePayment = et.SubElement(MessageHeader, 'GlobalGuaranteePayment')
        # GlobalGuaranteePayment.text = 'Y'

        counter =0
        # ManifestRecord Data 
        for row in raw_data.iterrows():
            counter +=1
            ManifestRecord = et.SubElement(root, 'ManifestRecord'            )
            ManifestHeader = et.SubElement(ManifestRecord, 'ManifestHeader')
            ManifestNo = et.SubElement(ManifestHeader, 'ManifestNo')
            ManifestNo.text = 'SVX-'+str(row[1]['FlightVoyageNumber'])+'-'+datetime.today().strftime('%d%m%Y')+'-1120' + str(counter)
            
            TransportMode = et.SubElement(ManifestHeader, 'TransportMode')
            TransportMode.text = 'A'
            # GeneralManifestNo = et.SubElement(ManifestHeader, 'GeneralManifestNo')
            # GeneralManifestNo.text = ''
            TransportDocType = et.SubElement(ManifestHeader, 'TransportDocType')
            TransportDocType.text = 'IN'

            PortOfDischarge = et.SubElement(ManifestHeader, 'PortOfDischarge')
            CountryCode = et.SubElement(PortOfDischarge, 'CountryCode')
            CountryCode.text = 'QA'
            PortCode = et.SubElement(PortOfDischarge, 'PortCode')
            PortCode.text = 'DOH'
            PortName = et.SubElement(PortOfDischarge, 'PortName')
            PortName.text = 'DOH'
            PortType = et.SubElement(PortOfDischarge, 'PortType')
            PortType.text = 'A'

            NumberofTrnDocs = et.SubElement(ManifestHeader, 'NumberofTrnDocs')
            NumberofTrnDocs.text = str(row[1]['NumberofTrnDocs'])
            NumberofContainers = et.SubElement(ManifestHeader, 'NumberofContainers')
            NumberofContainers.text = '0'

            # MeansOfTransport Data 
            MeansOfTransport = et.SubElement(ManifestRecord, 'MeansOfTransport')
            MeansofTransportNumber = et.SubElement(MeansOfTransport, 'MeansofTransportNumber')
            MeansofTransportNumber.text = str(row[1]['MeansofTransportNumber']).zfill(3)
            MeansofTransportName = et.SubElement(MeansOfTransport, 'MeansofTransportName')
            MeansofTransportName.text = str(row[1]['MeansofTransportName'])
            MeansofTransportNat = et.SubElement(MeansOfTransport, 'MeansofTransportNat')
            MeansofTransportNat.text = str(row[1]['MeansofTransportNat'])
            FlightVoyageNumber = et.SubElement(MeansOfTransport, 'FlightVoyageNumber')
            FlightVoyageNumber.text = str(row[1]['FlightVoyageNumber'])
            ETA = et.SubElement(MeansOfTransport, 'ETA')
            ETA.text = str(row[1]['ETA'])
            ETD = et.SubElement(MeansOfTransport, 'ETD')
            ETD.text = str(row[1]['ETD'])

            # TransportDocumentList Data 
            TransportDocumentList = et.SubElement(ManifestRecord, 'TransportDocumentList')

            TransportDocument = et.SubElement(TransportDocumentList, 'TransportDocument')

            # MasterTransportDocNumber = et.SubElement(TransportDocument, 'MasterTransportDocNumber')
            # MasterTransportDocNumber.text = str(row[1]['MasterTransportDocNumber'])            
            TransportDocNumber = et.SubElement(TransportDocument, 'TransportDocNumber')
            TransportDocNumber.text = str(row[1]['TransportDocNumber'])
            TotalQuantity = et.SubElement(TransportDocument, 'TotalQuantity')
            Quantity = et.SubElement(TotalQuantity, 'Quantity')
            Quantity.text = str(row[1]['TotalQuantity'])
            UOM = et.SubElement(TotalQuantity, 'UOM')
            UOM.text = 'PCS'
            TotalGrossWeight = et.SubElement(TransportDocument, 'TotalGrossWeight')
            Weight  = et.SubElement(TotalGrossWeight, 'Weight')
            Weight.text = str(row[1]['GrossWeight'])
            UOM = et.SubElement(TotalGrossWeight, 'UOM')
            UOM.text = 'KG'

            # PortofLoading = et.SubElement(TransportDocument, 'PortofLoading')
            # CountryCode = et.SubElement(PortofLoading, 'CountryCode')
            # CountryCode.text = str(row[1]['CountryCode'])
            # PortCode = et.SubElement(PortofLoading, 'PortCode')
            # PortCode.text = str(row[1]['PortCode'])
            # PortName = et.SubElement(PortofLoading, 'PortName')
            # PortName.text = str(row[1]['PortName'])
            # PortType = et.SubElement(PortofLoading, 'PortType')
            # PortType.text = str(row[1]['PortType'])

            FirstPortofLoading = et.SubElement(TransportDocument, 'FirstPortofLoading')
            CountryCode = et.SubElement(FirstPortofLoading, 'CountryCode')
            CountryCode.text = str(row[1]['LoadingCountryCode'])
            PortCode = et.SubElement(FirstPortofLoading, 'PortCode')
            PortCode.text = str(row[1]['LoadingPortCode'])
            PortName = et.SubElement(FirstPortofLoading, 'PortName')
            PortName.text = str(row[1]['LoadingPortName'])
            PortType = et.SubElement(FirstPortofLoading, 'PortType')
            PortType.text = 'A'
       
            PortofDischarge = et.SubElement(TransportDocument, 'PortofDischarge')
            CountryCode = et.SubElement(PortofDischarge, 'CountryCode')
            CountryCode.text = 'QA'
            PortCode = et.SubElement(PortofDischarge, 'PortCode')
            PortCode.text = 'DOH'
            PortName = et.SubElement(PortofDischarge, 'PortName')
            PortName.text = 'DOH'
            PortType = et.SubElement(PortofDischarge, 'PortType')
            PortType.text = 'A'

            FinalDestination  = et.SubElement(TransportDocument, 'FinalDestination')
            FinalDestination.text = 'QA'

            PartyList = et.SubElement(TransportDocument, 'PartyList')
            Party = et.SubElement(PartyList, 'Party')
            PartyType = et.SubElement(Party, 'PartyType')
            PartyType.text = '1'
            PartyName = et.SubElement(Party, 'PartyName')
            PartyName.text = str(row[1]['PartyName'])
            PartyAddress = et.SubElement(Party, 'PartyAddress')
            PartyAddress.text = str(row[1]['PartyAddress'])
            
            # ContainerList = et.SubElement(TransportDocument, 'ContainerList')
            # Container = et.SubElement(ContainerList, 'Container')
            # ContainerNumber = et.SubElement(Container, 'ContainerNumber')
            # ContainerType = et.SubElement(Container, 'ContainerType')
            # ContainerSize = et.SubElement(Container, 'ContainerSize')

            ItemList = et.SubElement(TransportDocument, 'ItemList')
            Item = et.SubElement(ItemList, 'Item')
            ItemDescription = et.SubElement(Item, 'ItemDescription')
            ItemDescription.text = str(row[1]['ItemDescription'])
            ItemCOO = et.SubElement(Item, 'ItemCOO')
            ItemCOO.text = str(row[1]['ItemCOO'])
            ItemQuantity = et.SubElement(Item, 'ItemQuantity')
            Quantity = et.SubElement(ItemQuantity, 'Quantity')
            Quantity.text = str(row[1]['ItemQuantity'])
            UOM = et.SubElement(ItemQuantity, 'UOM')
            UOM.text = 'PCS'
            ItemGrossWeight = et.SubElement(Item, 'ItemGrossWeight')
            Weight = et.SubElement(ItemGrossWeight, 'Weight')
            Weight.text = str(row[1]['ItemGrossWeight'])
            UOM = et.SubElement(ItemGrossWeight, 'UOM')
            UOM.text = 'KG'
            ItemPackagingType = et.SubElement(Item, 'ItemPackagingType')
            ItemPackagingType.text = 'OTH'
            ItemMarksNumbers = et.SubElement(Item, 'ItemMarksNumbers')
            ItemMarksNumbers.text = '910-55023641'
            # Master Airway Number
            ItemDGFlag = et.SubElement(Item, 'ItemDGFlag')
            ItemDGFlag.text = 'N'


            RouteList = et.SubElement(TransportDocument, 'RouteList')
            Route = et.SubElement(RouteList, 'Route')
            Port = et.SubElement(Route, 'Port')
            CountryCode = et.SubElement(Port, 'CountryCode')
            CountryCode.text = str(row[1]['LoadingCountryCode'])
            PortCode = et.SubElement(Port, 'PortCode')
            PortCode.text = str(row[1]['LoadingPortCode'])
            PortName = et.SubElement(Port, 'PortName')
            PortName.text = str(row[1]['LoadingPortName'])
            PortType = et.SubElement(Port, 'PortType')
            PortType.text = 'A'

            Route = et.SubElement(RouteList, 'Route')
            Port = et.SubElement(Route, 'Port')
            CountryCode = et.SubElement(Port, 'CountryCode')
            CountryCode.text = 'QA'
            PortCode = et.SubElement(Port, 'PortCode')
            PortCode.text = 'DOH'
            PortName = et.SubElement(Port, 'PortName')
            PortName.text = 'DOH'
            PortType = et.SubElement(Port, 'PortType')
            PortType.text = 'A'



        tree = et.ElementTree(root)
        et.indent(tree, space="\t", level=0)
        filename = 'SVX-DOH-'+datetime.today().strftime('%d%m%Y')+'-'+datetime.today().strftime('%H%M')+'.xml'
        tree.write(filename, encoding="utf-8")        


        # SFTP Conncetion 
        # srv = pysftp.Connection(host="86.62.248.233", username="2736798986565656", port=4848,
        #  password="Tests@34s#")
        # with srv.cd('public'): #chdir to public
        #      srv.put('filename') #upload file to nodejs/
        # # # Closes the connection
        # srv.close()
    
        # ssh = paramiko.SSHClient()

        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # ssh.connect('86.62.248.233', username='2736798986565656',port=4848, key_filename= './download/2736798986565656.ppk')

        # stdin, stdout, stderr = ssh.exec_command('ls')
        # print (stdout.readlines())
        # ssh.close()
        # with pysftp.Connection('86.62.248.233', port=4848 ,username='2736798986565656', private_key='./authorized_keys') as sftp:
        #     # upload file to current working directory of the sftp server
        #     # without changing the file modification time
        #     #sftp.put(filename, preserve_mtime=True)
            
        #     # upload file to different remote folder and file path
        #     sftp.put(filename, preserve_mtime=True, remotepath="/upload/{}".format(filename))
        #     # upload contents from local directory to remote directory
        #     #sftp.put_d(r"C:\path\to\localFolder", "./remoteFolder", preserve_mtime=True)
            
        #     # upload contents from local directory to remote directory and create intermediate folders if required
        #     #sftp.put_r(r"C:\path\to\localFolder", "./remoteFolder", preserve_mtime=True)
            
        #     print("copy completed!")

        
        

        return send_file(filename, as_attachment=True)
    else:
        return render_template('bulk.html')
            

@app.route('/bulkdeclaration', methods=['GET', 'POST'])
def bulkdeclaration():
    if request.method == 'POST':
        @after_this_request
        def delete_xml(response):
            target = '/app/'
            filelist = glob.glob(os.path.join(target, "*.xml"))
            for f in filelist:
                os.remove(f)
            return response

        f = f = request.files['declarationxlsfile']
        raw_data = pd.read_excel(f)
        
        xmlns = "/schema/declaration"
        xsi = "http://www.w3.org/2001/XMLSchema-instance"
        schemaLocation = "/schema/declaration_schema.xsd"
        
        root = et.Element(
            "{" + xmlns + "}CustomsDeclaration",
            attrib={"{" + xsi + "}schemaLocation": schemaLocation},
            nsmap={'xsi': xsi, None: xmlns}
        )

        # MessageHeader Data 
        MessageHeader = et.SubElement(root, 'MessageHeader')

        docType = et.SubElement(MessageHeader, 'docType')
        batchID = et.SubElement(MessageHeader, 'batchID')
        MessageSender = et.SubElement(MessageHeader, 'MessageSender')
        UserId = et.SubElement(MessageSender, 'UserId')
        MessageDate = et.SubElement(MessageHeader, 'MessageDate')
        MessageTime = et.SubElement(MessageHeader, 'MessageTime')

        docType.text = 'CUSDEC'
        batchID.text = 'qccsw1'
        UserId.text = '147504122018000'
        MessageDate.text = datetime.today().strftime('%d%m%Y')
        MessageTime.text = datetime.today().strftime('%H%M')

        # DeclarationRecord Data 
        for row in raw_data.iterrows():
            DeclarationRecord = et.SubElement(root, 'DeclarationRecord')
            Payload = et.SubElement(DeclarationRecord, 'Payload')
            Action = et.SubElement(Payload, 'Action')
            Action.text = str(row[1]['Action'])

            # DeclarationHeader Data 
            DeclarationHeader = et.SubElement(Payload, 'DeclarationHeader')

            DeclarationType = et.SubElement(DeclarationHeader, 'DeclarationType')
            CustomsOfficeofEntry = et.SubElement(DeclarationHeader, 'CustomsOfficeofEntry')
            CustomsOfficeofExit = et.SubElement(DeclarationHeader, 'CustomsOfficeofExit')
            StatisticalDecFlag = et.SubElement(DeclarationHeader, 'StatisticalDecFlag')
            OnsiteInspectionFlag = et.SubElement(DeclarationHeader, 'OnsiteInspectionFlag')
            ContainerTransportIndicator = et.SubElement(DeclarationHeader, 'ContainerTransportIndicator')
            # StrategicGoods = et.SubElement(DeclarationHeader, 'StrategicGoods')
            # Remarks = et.SubElement(DeclarationHeader, 'Remarks')
            CourierDeclaration = et.SubElement(DeclarationHeader, 'CourierDeclaration')
            ExpressCompanies = et.SubElement(DeclarationHeader, 'ExpressCompanies')
            ModeofPayment = et.SubElement(DeclarationHeader, 'ModeofPayment')
            GuaranteeAccount = et.SubElement(DeclarationHeader, 'GuaranteeAccount')

            DeclarationType.text = str(row[1]['DeclarationType'])
            CustomsOfficeofEntry.text = str(row[1]['CustomsOfficeofEntry'])
            CustomsOfficeofExit.text = str(row[1]['CustomsOfficeofExit'])
            StatisticalDecFlag.text = str(row[1]['StatisticalDecFlag'])
            OnsiteInspectionFlag.text = str(row[1]['OnsiteInspectionFlag'])
            ContainerTransportIndicator.text = str(row[1]['ContainerTransportIndicator'])
            # StrategicGoods.text = str(row[1]['StrategicGoods'])
            # Remarks.text = ''
            CourierDeclaration.text = str(row[1]['CourierDeclaration'])
            ExpressCompanies.text = str(row[1]['ExpressCompanies'])
            ModeofPayment.text = str(row[1]['ModeofPayment'])
            GuaranteeAccount.text = str(row[1]['GuaranteeAccount'])

            # Party Data 
            Party = et.SubElement(Payload, 'Party')

            Importer = et.SubElement(Party, 'Importer')
            ImporterCode  = et.SubElement(Importer, 'ImporterCode')
            ImporterName = et.SubElement(Importer, 'ImporterName')
            ImporterAddress = et.SubElement(Importer, 'ImporterAddress')
            ImporterPhone = et.SubElement(Importer, 'ImporterPhone')
            # ImporterIdType = et.SubElement(Importer, 'ImporterIdType')
            # ImporterIdNo = et.SubElement(Importer, 'ImporterIdNo')

            ImporterCode.text = str(row[1]['ImporterCode'])
            ImporterName.text = str(row[1]['ImporterName'])
            ImporterAddress.text = str(row[1]['ImporterAddress'])
            ImporterPhone.text = str(row[1]['ImporterPhone'])
            ImporterIdType = et.SubElement(Importer, 'ImporterIdType')
            ImporterIdType.text = str(row[1]['ImporterIdType']) 
            
            # ImporterIdType.text = str(row[1]['ImporterIdType'])
            # ImporterIdNo.text = str(row[1]['ImporterIdNo'])

            Exporter = et.SubElement(Party, 'Exporter')
            # ExporterCode = et.SubElement(Exporter, 'ExporterCode')
            ExporterName = et.SubElement(Exporter, 'ExporterName')
            ExporterAddress = et.SubElement(Exporter, 'ExporterAddress')
            ExporterPhoneNo = et.SubElement(Exporter, 'ExporterPhoneNo')

            # ExporterCode.text = ''
            ExporterName.text = str(row[1]['ExporterName'])
            ExporterAddress.text = str(row[1]['ExporterAddress'])
            ExporterPhoneNo.text = str(row[1]['ExporterPhoneNo'])

            ConsignorConsignee = et.SubElement(Party, 'ConsignorConsignee')
            ConsignorName = et.SubElement(ConsignorConsignee, 'ConsignorName')
            ConsignorName.text = str(row[1]['ConsignorName'])


            # # BoL Data 
            BillOfLading = et.SubElement(Payload, 'BillOfLading')
            CargoManifestNumber = et.SubElement(BillOfLading, 'CargoManifestNumber')
            CargoManifestNumber.text = str(row[1]['CargoManifestNumber'])
            MasterBLNumber = et.SubElement(BillOfLading, 'MasterBLNumber')
            MasterBLNumber.text = str(row[1]['MasterBLNumber'])
            HouseBLNumber = et.SubElement(BillOfLading, 'HouseBLNumber')
            HouseBLNumber.text = str(row[1]['HouseBLNumber'])
            PortOfLoading = et.SubElement(BillOfLading, 'PortOfLoading')
            PortOfLoading.text = str(row[1]['PortOfLoading'])
            DateofArrivalOrDeparture = et.SubElement(BillOfLading, 'DateofArrivalOrDeparture')
            DateofArrivalOrDeparture.text = str(row[1]['DateofArrivalOrDeparture'])
            FinalDestination = et.SubElement(BillOfLading, 'FinalDestination')
            FinalDestination.text = 'QA'
            TransportMeans = et.SubElement(BillOfLading, 'TransportMeans')
            Identification = et.SubElement(TransportMeans, 'Identification')
            Identification.text = str(row[1]['TransportMeansIdentification'])
            Name = et.SubElement(TransportMeans, 'Name')
            Name.text = str(row[1]['TransportMeansName'])
            Nationality = et.SubElement(TransportMeans, 'Nationality')
            Nationality.text = str(row[1]['TransportMeansNationality'])
            VoyageNumber = et.SubElement(TransportMeans, 'VoyageNumber')
            VoyageNumber.text = str(row[1]['VoyageNumber'])
            BLNumberOfPackages = et.SubElement(BillOfLading, 'BLNumberOfPackages')
            NumberOfPackages = et.SubElement(BLNumberOfPackages, 'NumberOfPackages')
            NumberOfPackages.text = str(row[1]['NumberOfPackages'])
            UOM = et.SubElement(BLNumberOfPackages, 'UOM')
            UOM.text = 'PCS'
            BLGrossWeight = et.SubElement(BillOfLading, 'BLGrossWeight')
            Weight = et.SubElement(BLGrossWeight, 'Weight')
            Weight.text = str(row[1]['BoLWeight'])
            UOM = et.SubElement(BLGrossWeight, 'UOM')
            UOM.text = 'KG'


            
            # # Containers Data 
            # Containers = et.SubElement(Payload, 'Containers')

            # Container = et.SubElement(Containers, 'Container')
            # ContainerNumber = et.SubElement(Container, 'ContainerNumber')
            # ContainerType = et.SubElement(Container, 'ContainerType')
            # ContainerWeight = et.SubElement(Container, 'ContainerWeight')
            # Weight = et.SubElement(ContainerWeight, 'Weight')
            # UOM = et.SubElement(ContainerWeight, 'UOM')
            # Weight.text = '1'
            # UOM.text = 'A'
            # TareWeight = et.SubElement(Container, 'TareWeight')
            # Weight = et.SubElement(TareWeight, 'Weight')
            # UOM = et.SubElement(TareWeight, 'UOM')
            # Weight.text = '1'
            # UOM.text = 'A'
            # ContainerNumber.text = ''
            # ContainerType.text = ''

            # # Seals Data 
            # Seals = et.SubElement(Payload, 'Seals')
            # Seal = et.SubElement(Seals, 'Seal')
            
            # SealNumber = et.SubElement(Seal, 'SealNumber')
            # SealNumber.text = ' '
            # CountryCode = et.SubElement(Seal, 'CountryCode')
            # CountryCode.text = 'QA'
            # ContainerNumber = et.SubElement(Seal, 'ContainerNumber')


            CertificateOfOrigins = et.SubElement(Payload, 'CertificateOfOrigins')
            certificateoforigin = et.SubElement(CertificateOfOrigins, 'certificateoforigin')
            CertificateNumber = et.SubElement(certificateoforigin, 'CertificateNumber')
            IssuanceDate = et.SubElement(certificateoforigin, 'IssuanceDate')
            CountryOfOriginCooList = et.SubElement(certificateoforigin, 'CountryOfOriginCooList')
            CountryOfOriginCoo = et.SubElement(CountryOfOriginCooList, 'CountryOfOriginCoo')
            CountryOfOriginCoo.text = str(row[1]['CountryOfOriginCoo'])
            CooTotalAmount = et.SubElement(certificateoforigin, 'CooTotalAmount')
            Amount =  et.SubElement(CooTotalAmount, 'Amount')
            CurrencyCoded = et.SubElement(CooTotalAmount, 'CurrencyCoded')
            Original = et.SubElement(certificateoforigin, 'Original')
            Attested = et.SubElement(certificateoforigin, 'Attested')
            CertificateNumber.text = str(row[1]['CoOCertificateNumber']).zfill(4)
            IssuanceDate.text = str(row[1]['IssuanceDate'])
            Amount.text = str(row[1]['CoOAmount'])
            CurrencyCoded.text = str(row[1]['CurrencyCoded'])
            Original.text = str(row[1]['Original'])
            Attested.text = str(row[1]['Attested'])
            


            Invoices = et.SubElement(Payload, 'Invoices')
            NumberOfCOONotAttested = et.SubElement(Invoices, 'NumberOfCOONotAttested')
            NumberOfCOONotOriginal = et.SubElement(Invoices, 'NumberOfCOONotOriginal')
            NumberOfCOONotAttested.text = str(row[1]['NumberOfCOONotAttested'])
            NumberOfCOONotOriginal.text = str(row[1]['NumberOfCOONotOriginal'])

            Invoice = et.SubElement(Invoices, 'Invoice')
            InvoiceNumber = et.SubElement(Invoice, 'InvoiceNumber')
            InvoiceDate = et.SubElement(Invoice, 'InvoiceDate')
            INCOTERMSCoded = et.SubElement(Invoice, 'INCOTERMSCoded')
            ConsignorName = et.SubElement(Invoice, 'ConsignorName')
            ConsignorAddress = et.SubElement(Invoice, 'ConsignorAddress')
            TotalInvoiceWeight = et.SubElement(Invoice, 'TotalInvoiceWeight')
            Weight = et.SubElement(TotalInvoiceWeight, 'Weight')
            Weight.text = str(row[1]['TotalInvoiceWeight'])
            UOM = et.SubElement(TotalInvoiceWeight, 'UOM')
            UOM.text = 'KG'
            InvoiceValue = et.SubElement(Invoice, 'InvoiceValue')
            Amount = et.SubElement(InvoiceValue, 'Amount')
            Amount.text = str(row[1]['InvoiceValue'])
            CurrencyCoded = et.SubElement(InvoiceValue, 'CurrencyCoded')
            CurrencyCoded.text = str(row[1]['InvCurrency'])
            # FreightCosts = et.SubElement(Invoice, 'FreightCosts')
            # Amount = et.SubElement(FreightCosts, 'Amount')
            # Amount.text = str(row[1]['FreightCosts'])
            # CurrencyCoded = et.SubElement(FreightCosts, 'CurrencyCoded')
            # CurrencyCoded.text = str(row[1]['FrgCurrency'])
            
            if str(row[1]['InsuranceCosts']) not in [None, 'nan', nan]:
                InsuranceCosts = et.SubElement(Invoice, 'InsuranceCosts')
                Amount = et.SubElement(InsuranceCosts, 'Amount')
                Amount.text = str(round(row[1]['InsuranceCosts'], 3))
                CurrencyCoded = et.SubElement(InsuranceCosts, 'CurrencyCoded')
                CurrencyCoded.text ='sddd'
            
            IsInvoiceOriginal = et.SubElement(Invoice, 'IsInvoiceOriginal')
            AuthenticationOfEmbassyConsulate = et.SubElement(Invoice, 'AuthenticationOfEmbassyConsulate')
            
            InvoiceNumber.text = str(row[1]['InvoiceNumber'])
            InvoiceDate.text = str(row[1]['InvoiceDate'])
            INCOTERMSCoded.text = str(row[1]['INCOTERMSCoded'])
            ConsignorName.text = str(row[1]['InvConsignorName'])
            ConsignorAddress.text = str(row[1]['ConsignorAddress'])
            IsInvoiceOriginal.text = str(row[1]['IsInvoiceOriginal'])
            AuthenticationOfEmbassyConsulate.text = str(row[1]['AuthenticationOfEmbassyConsulate'])
            CertificateNumber = et.SubElement(Invoice, 'CertificateNumber')
            CertificateNumber.text = str(row[1]['CoOCertificateNumber']).zfill(4)
            

            # # Item Data
            Items = et.SubElement(Payload, 'Items')
            LineItem = et.SubElement(Items, 'LineItem')

            TariffCodeNumber = et.SubElement(LineItem, 'TariffCodeNumber')
            TariffCodeNumber.text = str(row[1]['ItemTariff'])
            # ItemDescriptionAdditional = et.SubElement(LineItem, 'ItemDescriptionAdditional')
            # ItemDescriptionAdditional.text = ' '
            CountryofOriginCoded = et.SubElement(LineItem, 'CountryofOriginCoded')
            CountryofOriginCoded.text = str(row[1]['CountryofOriginCoded'])

            # VehicleDetails = et.SubElement(LineItem, 'VehicleDetails')
            # ChassisNumber = et.SubElement(VehicleDetails, 'ChassisNumber')
            # VehicleMake = et.SubElement(VehicleDetails, 'VehicleMake')
            # VehicleModel = et.SubElement(VehicleDetails, 'VehicleModel')
            # VehicleCategory = et.SubElement(VehicleDetails, 'VehicleCategory')
            # ModelYear = et.SubElement(VehicleDetails, 'ModelYear')
            # Color = et.SubElement(VehicleDetails, 'Color')
            # EngineNumber = et.SubElement(VehicleDetails, 'EngineNumber')
            # EngineCapacity = et.SubElement(VehicleDetails, 'EngineCapacity')
            # ManufacturingDate = et.SubElement(VehicleDetails, 'ManufacturingDate')
            # VehicleCondition = et.SubElement(VehicleDetails, 'VehicleCondition')
            # NumberOfCylinders = et.SubElement(VehicleDetails, 'NumberOfCylinders')

            # ChassisNumber.text = 'string'
            # VehicleMake.text = 'string'
            # VehicleModel.text = 'string'
            # VehicleCategory.text = 'stonk'
            # ModelYear.text = '1997'
            # Color.text = 'string'
            # EngineNumber.text = 'string'
            # EngineCapacity.text = 'string'
            # ManufacturingDate.text = '1995-09-10'
            # VehicleCondition.text = 'NEW'
            # NumberOfCylinders.text = '42'

            AdditionalInformation = et.SubElement(LineItem, 'AdditionalInformation')
            Brand = et.SubElement(AdditionalInformation, 'Brand')
            Brand.text = str(row[1]['Brand'])
            # Model = et.SubElement(AdditionalInformation, 'Model')
            # ProductionYear = et.SubElement(AdditionalInformation, 'ProductionYear')
            # ProductionYear.text = str(row[1]['ProductionYear'])

            # Volume = et.SubElement(AdditionalInformation, 'Volume')
            # Value = et.SubElement(Volume, 'Value')
            # Value.text = str(row[1]['Size'])
            # UOM = et.SubElement(Volume, 'UOM')
            # UOM.text = 'CBM'

            ItemGrossWeight = et.SubElement(LineItem, 'ItemGrossWeight')
            Weight = et.SubElement(ItemGrossWeight, 'Weight')
            UOM = et.SubElement(ItemGrossWeight, 'UOM')
            Weight.text = str(row[1]['ItemGrossWeight'])
            UOM.text = 'KG'

            ItemNetWeight = et.SubElement(LineItem, 'ItemNetWeight')
            Weight = et.SubElement(ItemNetWeight, 'Weight')
            UOM = et.SubElement(ItemNetWeight, 'UOM')
            Weight.text = str(row[1]['ItemNetWeight'])
            UOM.text = 'KG'

            ItemQuantity = et.SubElement(LineItem, 'ItemQuantity')
            Quantity = et.SubElement(ItemQuantity, 'Quantity')
            UOM = et.SubElement(ItemQuantity, 'UOM')
            Quantity.text = str(row[1]['ItemQuantity'])
            UOM.text = 'PCS'
            InvoiceNumber = et.SubElement(LineItem, 'InvoiceNumber')
            InvoiceNumber.text = str(row[1]['InvoiceNumber'])
            
            ItemValue = et.SubElement(LineItem, 'ItemValue')
            ItemDeclaredValue = et.SubElement(ItemValue, 'ItemDeclaredValue')
            Amount = et.SubElement(ItemDeclaredValue, 'Amount')
            Amount.text = str(row[1]['ItemDeclaredValue'])
            CurrencyCoded = et.SubElement(ItemDeclaredValue, 'CurrencyCoded')
            CurrencyCoded.text = str(row[1]['ItemCurrency'])

            Exemption = et.SubElement(LineItem, 'Exemption')
            ExemptionTypeCoded = et.SubElement(Exemption, 'ExemptionTypeCoded')
            ApprovalNumber = et.SubElement(Exemption, 'ApprovalNumber')
            ExemptionTypeCoded.text = str(row[1]['ExemptionTypeCoded'])
            ApprovalNumber.text = str(row[1]['ApprovalNumber'])

            # FreeOfCostQuantity = et.SubElement(LineItem, 'FreeOfCostQuantity')
            # Quantity = et.SubElement(FreeOfCostQuantity, 'Quantity')
            # Quantity.text = '2080000.2349058'

            # Shortage = et.SubElement(LineItem, 'Shortage')
            # Shortage.text = 'N'

            # ShortageQuantity = et.SubElement(LineItem, 'ShortageQuantity')
            # ShortageQuantity.text = '2477340.2349058'

            # RefDeclarationNumber = et.SubElement(LineItem, 'RefDeclarationNumber')
            # RefDeclarationNumber.text = 'string'

            CargoType = et.SubElement(LineItem, 'CargoType')
            CargoType.text = str(row[1]['CargoType'])

        tree = et.ElementTree(root)
        et.indent(tree, space="\t", level=0)
        filename = 'SVX-DOH-'+datetime.today().strftime('%d%m%Y')+'-'+datetime.today().strftime('%H%M')+'.xml'
        tree.write(filename, encoding="utf-8")        

        # SFTP Conncetion 
        # srv = pysftp.Connection(host="86.62.248.233", username="2736798986565656", port=4848
        # password="Tests@34s#",log="./temp/pysftp.log")
        # with srv.cd('public'): #chdir to public
        #     srv.put('filename') #upload file to nodejs/
        # # Closes the connection
        # srv.close()

        return send_file(filename, as_attachment=True)

        
    else:
            return render_template('bulk.html')

@app.route('/manifest-excel')
def manifestexcel():
    # target = '/app/'
    return send_file('download/CM.xlsx', as_attachment=True)

@app.route('/declaration-excel')
def declarationexcel():
    return send_file('download/DEC.xlsx', as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    # app.run(debug=True, port=port)