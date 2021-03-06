import FWCore.ParameterSet.Config as cms
from TrackingTools.TransientTrack.TransientTrackBuilder_cfi import *
from TrackingTools.GeomPropagators.SmartPropagator_cff import *
from TrackingTools.MaterialEffects.MaterialPropagator_cfi import *
from TrackingTools.MaterialEffects.OppositeMaterialPropagator_cfi import *
from PhysicsTools.PatAlgos.patSequences_cff import *
from PhysicsTools.PatAlgos.slimming.unpackedPatTrigger_cfi import unpackedPatTrigger
#from PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cfi import *
#from PhysicsTools.PatAlgos.triggerLayer1.triggerEventProducer_cfi import *
#from PhysicsTools.PatAlgos.triggerLayer1.triggerMatcher_cfi import * -- deprecated in 73


muonMatch = muonMatch.clone(
    src = cms.InputTag("slimmedMuons"),
    resolveByMatchQuality = cms.bool(True),
    matched = cms.InputTag("prunedGenParticles"),
)
patMuons = patMuons.clone(
    muonSource = cms.InputTag("slimmedMuons"),
    genParticleMatch = cms.InputTag("muonMatch"),
    addTeVRefits = cms.bool(False),
    embedTrack = cms.bool(True),
    embedCombinedMuon = cms.bool(True),
    embedStandAloneMuon = cms.bool(True),
    embedPickyMuon = cms.bool(False),
    embedTpfmsMuon = cms.bool(False),
    embedHighLevelSelection = cms.bool(True),
    usePV = cms.bool(True),
    beamLineSrc = cms.InputTag("offlineBeamSpot"),
    pvSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
    isolation = cms.PSet(),
    isoDeposits = cms.PSet(),
    embedCaloMETMuonCorrs = cms.bool(False),
    embedTcMETMuonCorrs = cms.bool(False),
)

# Tracker Muons Part
selectedPatTrackerMuons = selectedPatMuons.clone(
    src = cms.InputTag("slimmedMuons"),
    cut = cms.string("pt > 5.0 && isTrackerMuon() && numberOfMatches() > 1 && -2.4 < eta() && eta() < 2.4")
)
cleanPatTrackerMuons = cleanPatMuons.clone(
    src = cms.InputTag("selectedPatTrackerMuons")
)
countPatTrackerMuons = countPatMuons.clone(
    src = cms.InputTag("cleanPatTrackerMuons")
)
# PF Muons Part
selectedPatPFMuons = selectedPatMuons.clone(
    src = cms.InputTag("slimmedMuons"),
    #"Loose Muon" requirement on PF muons as recommended by Muon POG:
    #https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonId#Loose_Muon
    cut = cms.string("pt > 5.0 && isPFMuon() && ( isTrackerMuon() || isGlobalMuon() ) && -2.4 < eta() && eta() < 2.4")
)
cleanPatPFMuons = cleanPatMuons.clone(

    src = cms.InputTag("selectedPatPFMuons")
)
countPatPFMuons = countPatMuons.clone(
    src = cms.InputTag("cleanPatPFMuons")
)

# This module is derived from from https://github.com/cms-sw/cmssw/blob/CMSSW_7_3_X/PhysicsTools/PatAlgos/python/triggerLayer1/triggerMatcherExamples_cfi.py
cleanMuonTriggerMatchHLTMu17 = cms.EDProducer("PATTriggerMatcherDRDPtLessByR", # match by DeltaR only, best match by DeltaR
    src     = cms.InputTag( "cleanPatMuons" ),
   # src     = cms.InputTag( "slimmedMuons" ),
    matched = cms.InputTag( "unpackedPatTrigger" ),  # default producer label as defined in PhysicsTools/PatAlgos/python/triggerLayer1/triggerProducer_cfi.py
    matchedCuts = cms.string( 'path( "HLT_Mu17_v*" )' ),
    maxDPtRel = cms.double( 0.5 ),
    maxDeltaR = cms.double( 0.5 ),
    resolveAmbiguities    = cms.bool( True ),        # only one match per trigger object
    resolveByMatchQuality = cms.bool( True )        # take best match found per reco object: by DeltaR here (s. above)
)


# Trigger match
#    First matcher from PhysicsTools/PatAlgos/python/triggerLayer1/triggerMatcher_cfi.py
#    is cleanMuonTriggerMatchHLTMu17 . Clone it!
#    Note in 2012 wildcard HLT_Mu* includes ONLY muon trigger. No more HLT_MultiVertex6 and such!
# This is trigger match for Tracker muons
cleanTrackerMuonTriggerMatchHLTMu = cleanMuonTriggerMatchHLTMu17.clone(
    src = cms.InputTag( "cleanPatTrackerMuons" ),
 #  src = cms.InputTag( "slimmedMuons" ), 
 #  matched = cms.InputTag( "selectedPatTrigger" ),
   matchedCuts = cms.string('path("HLT_Mu*")')
)
cleanTrackerMuonTriggerMatchHLTIsoMu = cleanMuonTriggerMatchHLTMu17.clone(
    src = cms.InputTag( "cleanPatTrackerMuons" ),
  #  src = cms.InputTag( "slimmedMuons" ),
    matchedCuts = cms.string('path("HLT_IsoMu*")')
)
cleanTrackerMuonTriggerMatchHLTDoubleMu = cleanMuonTriggerMatchHLTMu17.clone(
    src = cms.InputTag( "cleanPatTrackerMuons" ),
   # src = cms.InputTag( "slimmedMuons" ),
    matchedCuts = cms.string('path("HLT_DoubleMu*_v*")')
)
cleanTrackerMuonTriggerMatchHLTTrkMu15DoubleTrkMu5 = cleanMuonTriggerMatchHLTMu17.clone(
    src = cms.InputTag( "cleanPatTrackerMuons" ),
 #   src = cms.InputTag( "slimmedMuons" ),
    matchedCuts = cms.string('path("HLT_TrkMu15_DoubleTrkMu5NoFiltersNoVtx_v*")')
)
cleanTrackerMuonTriggerMatchHLTTrkMu17DoubleTrkMu8 = cleanMuonTriggerMatchHLTMu17.clone(
    src = cms.InputTag( "cleanPatTrackerMuons" ),
 #   src = cms.InputTag( "slimmedMuons" ),
    matchedCuts = cms.string('path("HLT_TrkMu17_DoubleTrkMu8NoFiltersNoVtx_v*")')
)
cleanPatTrackerMuonsTriggerMatch = cms.EDProducer("PATTriggerMatchMuonEmbedder",
    src = cms.InputTag("cleanPatTrackerMuons"),
 #   src = cms.InputTag( "slimmedMuons" ),  
    matches = cms.VInputTag("cleanTrackerMuonTriggerMatchHLTMu",
                            "cleanTrackerMuonTriggerMatchHLTIsoMu",
                            "cleanTrackerMuonTriggerMatchHLTDoubleMu",
                            "cleanTrackerMuonTriggerMatchHLTTrkMu15DoubleTrkMu5",
                            "cleanTrackerMuonTriggerMatchHLTTrkMu17DoubleTrkMu8")
)



# This is trigger match for PF muons
cleanPFMuonTriggerMatchHLTMu = cleanMuonTriggerMatchHLTMu17.clone(
    src = cms.InputTag( "cleanPatPFMuons" ),
   # src = cms.InputTag( "slimmedMuons" ),
    matchedCuts = cms.string('path("HLT_Mu*")')
) 
cleanPFMuonTriggerMatchHLTIsoMu = cleanMuonTriggerMatchHLTMu17.clone(
    src = cms.InputTag( "cleanPatPFMuons" ),
   # src = cms.InputTag( "slimmedMuons" ),  
    matchedCuts = cms.string('path("HLT_IsoMu*")')
)
cleanPFMuonTriggerMatchHLTDoubleMu = cleanMuonTriggerMatchHLTMu17.clone(
    src = cms.InputTag( "cleanPatPFMuons" ),
 #   src = cms.InputTag( "slimmedMuons" ),
    matchedCuts = cms.string('path("HLT_DoubleMu*_v*")')
)
cleanPFMuonTriggerMatchHLTTrkMu15DoubleTrkMu5 = cleanMuonTriggerMatchHLTMu17.clone(
    src = cms.InputTag( "cleanPatPFMuons" ),
 #   src = cms.InputTag( "slimmedMuons" ),
    matchedCuts = cms.string('path("HLT_TrkMu15_DoubleTrkMu5NoFiltersNoVtx_v*")')
)   
cleanPFMuonTriggerMatchHLTTrkMu17DoubleTrkMu8 = cleanMuonTriggerMatchHLTMu17.clone(
    src = cms.InputTag( "cleanPatPFMuons" ),
   # src = cms.InputTag( "slimmedMuons" ),
    matchedCuts = cms.string('path("HLT_TrkMu17_DoubleTrkMu8NoFiltersNoVtx_v*")')
)   
cleanPatPFMuonsTriggerMatch = cms.EDProducer("PATTriggerMatchMuonEmbedder",
    src = cms.InputTag("cleanPatPFMuons"),
 #   src = cms.InputTag( "slimmedMuons" ),
    matches = cms.VInputTag("cleanPFMuonTriggerMatchHLTMu",
                            "cleanPFMuonTriggerMatchHLTIsoMu",
                            "cleanPFMuonTriggerMatchHLTDoubleMu",
                            "cleanPFMuonTriggerMatchHLTTrkMu15DoubleTrkMu5",
                            "cleanPFMuonTriggerMatchHLTTrkMu17DoubleTrkMu8")
)
patifyTrackerMuon = cms.Sequence(
    selectedPatTrackerMuons * 
    cleanPatTrackerMuons * 
    countPatTrackerMuons * 
    cleanTrackerMuonTriggerMatchHLTMu * 
    cleanTrackerMuonTriggerMatchHLTIsoMu * 
    cleanTrackerMuonTriggerMatchHLTDoubleMu * 
    cleanTrackerMuonTriggerMatchHLTTrkMu15DoubleTrkMu5 *
    cleanTrackerMuonTriggerMatchHLTTrkMu17DoubleTrkMu8 *
    cleanPatTrackerMuonsTriggerMatch
)
patifyPFMuon = cms.Sequence(
    selectedPatPFMuons * 
    cleanPatPFMuons * 
    countPatPFMuons * 
    cleanPFMuonTriggerMatchHLTMu * 
    cleanPFMuonTriggerMatchHLTIsoMu * 
    cleanPFMuonTriggerMatchHLTDoubleMu * 
    cleanPFMuonTriggerMatchHLTTrkMu15DoubleTrkMu5 *
    cleanPFMuonTriggerMatchHLTTrkMu17DoubleTrkMu8 *
    cleanPatPFMuonsTriggerMatch
)

patifyData = cms.Sequence(
 #   patMuons * 
  #  patTrigger * 
#    patTriggerEvent * 
    unpackedPatTrigger *
    patifyTrackerMuon * 
    patifyPFMuon
)
patifyMC = cms.Sequence(
    muonMatch * 
    patifyData
)

patDefaultSequence = cms.Sequence()
patCandidates = cms.Sequence()
makePatMuons = cms.Sequence()

