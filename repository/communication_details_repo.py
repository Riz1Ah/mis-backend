from utils import connector

from models import communication_details_model as cdm

def get_data_repo():

  query = """

    with cte_data as

    (

    select policy_no FROM temp_SR_117244_Policy

    )

    ----- Retail Data Against Policy No-------------

    select Segment,Policy_Number,BA_No,SALUTATION,Proposer_Name,Proposer_Date_of_Birth,Proposer_PAN_No,ADDRESSLINE1,ADDRESSLINE2,ADDRESSLINE3,CITY,DISTRICT,STATE,PINCODE

    ,MOBILE_NUMBER,Email_Address

    from

    (

    select DISTINCT

    'Retail' Segment,

    pol.Policynum Policy_Number,

    pol.proposalnum as BA_No,

    c.TITLECD SALUTATION,

    c.FIRSTNAME1 || ' ' || c.LASTNAME1 as Proposer_Name,

    c.birthdt as Proposer_Date_of_Birth

    ,pi.IDENTITYNUM as Proposer_PAN_No

    ,d.ADDRESSLINE1LANG1 ADDRESSLINE1,d.ADDRESSLINE2LANG1 ADDRESSLINE2,d.ADDRESSLINE3LANG1 ADDRESSLINE3,

    CITYCD CITY,DISTRICTCD DISTRICT,STATECD STATE,d.PINCODE

    ,coalesce(F1.CONTACTNUM,F2.CONTACTNUM) AS MOBILE_NUMBER, coalesce(E1.EMAILADDRESS,E2.EMAILADDRESS) as Email_Address

    ,row_number() over (partition by policynum order by renewalyear desc) rn

    from cigna_datalake.datalake_dea_tab_policy_history pol

    inner join cte_data on cte_data.policy_no = pol.Policynum

    inner join cigna_datalake.datalake_dea_tab_policypartyrole b on pol.policyseq=b.policyseq

    inner join cigna_datalake.datalake_dea_tab_party c on b.partyid=c.partyid and b.ROLECD='PROPOSER'

    inner join cigna_datalake.datalake_dea_tab_partyaddress d on c.partyseq=d.partyseq and ADDRESSTYPECD='COMMUNICATION'

    LEFT join cigna_datalake.datalake_dea_tab_partyEMAIL E1 on C.partyseq=E1.partyseq AND E1.EMAILTYPECD='PERSONAL'

    LEFT join cigna_datalake.datalake_dea_tab_partyEMAIL E2 on C.partyseq=E2.partyseq AND E2.EMAILTYPECD='ALTERNATE'

    left join cigna_datalake.datalake_dea_tab_PARTYCONTACT F1 on c.partyseq=F1.partyseq AND F1.CONTACTTYPECD='MOBILE'

    left join cigna_datalake.datalake_dea_tab_PARTYCONTACT F2 on c.partyseq=F2.partyseq AND (F2.CONTACTTYPECD='OFFICE' OR F2.CONTACTTYPECD='RESIDENTIAL')

    LEFT join cigna_datalake.datalake_dea_tab_partyidentity pi on pi.partyseq=c.partyseq AND pi.IDENTITYTYPECD='PAN'

    where b.ROLECD='PROPOSER' and statuscd is not null

    ) x

    where x.rn = 1

    union

    ----- Retail Data Against BA No-------------

    select Segment,Policy_Number,BA_No,SALUTATION,Proposer_Name,Proposer_Date_of_Birth,Proposer_PAN_No,ADDRESSLINE1,ADDRESSLINE2,ADDRESSLINE3,CITY,DISTRICT,STATE,PINCODE

    ,MOBILE_NUMBER,Email_Address

    from

    (

    select DISTINCT

    'Retail' Segment,

    pol.Policynum Policy_Number,pol.proposalnum as BA_No,c.TITLECD SALUTATION,c.FIRSTNAME1 || ' ' || c.LASTNAME1 as Proposer_Name

    ,c.birthdt as Proposer_Date_of_Birth

    ,pi.IDENTITYNUM as Proposer_PAN_No

    ,d.ADDRESSLINE1LANG1 ADDRESSLINE1,d.ADDRESSLINE2LANG1 ADDRESSLINE2,d.ADDRESSLINE3LANG1 ADDRESSLINE3,

    CITYCD CITY,DISTRICTCD DISTRICT,STATECD STATE,d.PINCODE

    ,coalesce(F1.CONTACTNUM,F2.CONTACTNUM) AS MOBILE_NUMBER, coalesce(E1.EMAILADDRESS,E2.EMAILADDRESS) as Email_Address

    ,row_number() over (partition by policynum order by renewalyear desc) rn

    from cigna_datalake.datalake_dea_tab_policy pol

    inner join cte_data on cte_data.policy_no = pol.proposalnum

    inner join cigna_datalake.datalake_dea_tab_policypartyrole b on pol.policyseq=b.policyseq

    inner join cigna_datalake.datalake_dea_tab_party c on b.partyid=c.partyid and b.ROLECD='PROPOSER'

    inner join cigna_datalake.datalake_dea_tab_partyaddress d on c.partyseq=d.partyseq and ADDRESSTYPECD='COMMUNICATION'

    LEFT join cigna_datalake.datalake_dea_tab_partyEMAIL E1 on C.partyseq=E1.partyseq AND E1.EMAILTYPECD='PERSONAL'

    LEFT join cigna_datalake.datalake_dea_tab_partyEMAIL E2 on C.partyseq=E2.partyseq AND E2.EMAILTYPECD='ALTERNATE'

    left join cigna_datalake.datalake_dea_tab_PARTYCONTACT F1 on c.partyseq=F1.partyseq AND F1.CONTACTTYPECD='MOBILE'

    left join cigna_datalake.datalake_dea_tab_PARTYCONTACT F2 on c.partyseq=F2.partyseq AND (F2.CONTACTTYPECD='OFFICE' OR F2.CONTACTTYPECD='RESIDENTIAL')

    left join cigna_datalake.datalake_dea_tab_product P on POL.BASEPRODUCTID=P.PRODUCTID

    LEFT join cigna_datalake.datalake_dea_tab_partyidentity pi on pi.partyseq=c.partyseq AND pi.IDENTITYTYPECD='PAN'

    where b.ROLECD='PROPOSER' and statuscd is not null

    ) x

    where x.rn = 1

    """

  df = connector.fetchQuery(query, cdm.get_model())

  return df







