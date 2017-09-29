import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *

finalIsolatedTracks = cms.EDProducer("IsolatedTrackCleaner",
    tracks = cms.InputTag("isolatedTracks"),
    cut = cms.string("((pt>5 && (abs(pdgId) == 11 || abs(pdgId) == 13)) || pt > 10) && (abs(pdgId) < 15 || abs(eta) < 2.5) && abs(dxy) < 0.2 && abs(dz) < 0.1 && isHighPurityTrack && ((pfIsolationDR03().chargedHadronIso < 5 && pt < 25) || pfIsolationDR03().chargedHadronIso/pt < 0.2)"), 
    finalLeptons = cms.VInputTag(
        cms.InputTag("finalElectrons"),
        cms.InputTag("finalMuons"),
    ),
)

isoForIsoTk = cms.EDProducer("IsoTrackIsoValueMapProducer",
    src = cms.InputTag("finalIsolatedTracks"),
    rho_MiniIso = cms.InputTag("fixedGridRhoFastjetCentralNeutral"),
    EAFile_MiniIso = cms.FileInPath("PhysicsTools/NanoAOD/data/effAreaMuons_cone03_pfNeuHadronsAndPhotons_80X.txt"),
)

isoTrackTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("finalIsolatedTracks"),
    cut = cms.string(""), # filtered already above
    name = cms.string("IsoTrack"),
    doc  = cms.string("isolated tracks after basic selection (" + finalIsolatedTracks.cut.value() + ") and lepton veto"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the muons
    variables = cms.PSet(P3Vars,
        dz = Var("dz",float,doc="dz (with sign) wrt first PV, in cm",precision=10),
        dxy = Var("dxy",float,doc="dxy (with sign) wrt first PV, in cm",precision=10),
	isPFcand = Var("?packedCandRef().isNonnull()?1:0",int,doc="if isolated track is a PF candidate"),
	pdgId = Var("pdgId",int,doc="PDG id of PF cand"),
        PFIso03_chg = Var("pfIsolationDR03().chargedHadronIso",float,doc="PF isolation dR=0.3, charged component",precision=10),
        PFIso03_all = Var("(pfIsolationDR03().chargedHadronIso + max(pfIsolationDR03().neutralHadronIso + pfIsolationDR03().photonIso - pfIsolationDR03().puChargedHadronIso/2,0.0))",float,doc="PF isolation dR=0.3, total (deltaBeta corrections)",precision=10),
    ),
    externalVariables = cms.PSet(
        miniPFIso_chg = ExtVar("isoForIsoTk:miniIsoChg",float,doc="mini PF isolation, charged component",precision=10),
        miniPFIso_all = ExtVar("isoForIsoTk:miniIsoAll",float,doc="mini PF isolation, total (with scaled rho*EA PU corrections)",precision=10),
    ),
)#

isoTrackSequence = cms.Sequence(finalIsolatedTracks + isoForIsoTk)
isoTrackTables = cms.Sequence(isoTrackTable)

