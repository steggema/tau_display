import ROOT
from DataFormats.FWLite import Events, Handle
from Display import *

# Based on initial code by Michalis Bachtis

hfH  = Handle ('std::vector<reco::PFRecHit>')
ecalH  = Handle ('std::vector<reco::PFRecHit>')
hcalH  = Handle ('std::vector<reco::PFRecHit>')
genParticlesH  = Handle ('std::vector<reco::GenParticle>')
# tracksH  = Handle ('std::vector<reco::PFRecTrack>')
ecalClustersH  = Handle ('std::vector<reco::PFCluster>')
hcalClustersH  = Handle ('std::vector<reco::PFCluster>')

tauH = Handle('std::vector<reco::PFTau>')

jetH = Handle('std::vector<reco::PFJet>')
genJetH = Handle('std::vector<reco::GenJet>')

ecalHitsBarrelH = Handle('edm::SortedCollection<EcalRecHit,edm::StrictWeakOrdering<EcalRecHit> >')
ecalHitsEndcapH = Handle('edm::SortedCollection<EcalRecHit,edm::StrictWeakOrdering<EcalRecHit> >')

# handlePFSim = Handle('std::vector<reco::PFSimParticle>')
# labelPFSim = ('particleFlowSimParticle')

events = Events('yuta.root')

for event in events:
    # event.getByLabel('particleFlowRecHitHO',hfH)
    event.getByLabel('particleFlowRecHitECAL',ecalH)
    event.getByLabel('particleFlowRecHitHBHE',hcalH)
    event.getByLabel('genParticles',genParticlesH)
    # event.getByLabel('pfTrack',tracksH)
    event.getByLabel('particleFlowClusterECAL',ecalClustersH)
    event.getByLabel('particleFlowClusterHBHE', hcalClustersH)
   
    event.getByLabel('ak5PFJets', jetH)
    event.getByLabel('ak5GenJets', genJetH)

    event.getByLabel("reducedEcalRecHitsEB", ecalHitsBarrelH)
    event.getByLabel("reducedEcalRecHitsEE", ecalHitsEndcapH)

    event.getByLabel("hpsPFTauProducer", tauH)

    # hf = hfH.product()
    ecal = ecalH.product()
    hcal = hcalH.product()
    genParticles = genParticlesH.product()
    # tracks = tracksH.product()
    ecalClusters = ecalClustersH.product()
    hcalClusters = hcalClustersH.product()

    taus = tauH.product()

    genTaus = [p for p in genParticles if abs(p.pdgId()) == 15]
    genPhotons = [p for p in genParticles if abs(p.pdgId()) == 22]
    genChargedPions = [p for p in genParticles if abs(p.pdgId()) == 211]

    genJets = genJetH.product()
    genJets = [j for j in genJets if j.pt()>20. and abs(j.eta())<2.5]

    hitsBarrel = ecalHitsBarrelH.product()
    hitsEndcap = ecalHitsEndcapH.product()

    jets = jetH.product()

    #find taus:
    for genParticle in genTaus:
        print '### Gen tau info'
        print 'N charged pions', len(genChargedPions)
        print 'N photons', len(genPhotons), '\n'


        foundGreatTau = False

        for tau in taus:
            if deltaR(tau.eta(), tau.phi(), genParticle.eta(), genParticle.phi()) < 0.5:
                print '### Matched tau'
                print 'Decay mode', tau.decayMode()
                if tau.decayMode() >= 0:
                    foundGreatTau = True
                print 'Signal pi zeros', len(tau.signalPiZeroCandidates())
                print 'mass', tau.mass()
                print
                print 'Iso pi zeros', len(tau.isolationPiZeroCandidates())
                print 'Iso photons', len(tau.isolationPFGammaCands())
                print
                print 'Iso neutral hadrons', len(tau.isolationPFNeutrHadrCands())
                print 'Iso charged hadrons', len(tau.isolationPFChargedHadrCands())
                print

        if not foundGreatTau:
            continue

        displayECAL = DisplayManager('ECAL', genParticle.eta(), genParticle.phi(), 0.5)
        displayHCAL = DisplayManager('HCAL', genParticle.eta(), genParticle.phi(), 0.5)



        #reloop on gen particles and add them in view
        for genP in genParticles:
            # if genP.status()!=1:
            #     continue
            # displayHCAL.addGenParticle(particle) 
            displayECAL.addGenParticle(genP) 
            displayHCAL.addGenParticle(genP) 
            # displayAll.addGenParticle(particle)

        #add HF hits    
        # for hit in hf:
        #     id = ROOT.HcalDetId(hit.detId())
        #     displayHCAL.addRecHit(hit,id.depth())
        #     displayAll.addRecHit(hit,id.depth())
        

        #add HCAL hits    
        for hit in hcal:
             id = ROOT.HcalDetId(hit.detId())
             displayHCAL.addRecHit(hit,id.depth())
             # displayAll.addRecHit(hit,id.depth())

        #add ECAL hits    
        for hit in ecal:
            displayECAL.addRecHit(hit,1)
            # displayAll.addRecHit(hit,1)

        for cluster in ecalClusters:
            displayECAL.addCluster(cluster, links=True)

        for cluster in hcalClusters:
            displayHCAL.addCluster(cluster, links=True)

        # #Add tracks
        # for track in tracks:
        #     displayHCAL.addTrack(track) 
        #     displayECAL.addTrack(track) 
        #     displayAll.addTrack(track)


        displayECAL.viewEtaPhi()    
        displayHCAL.viewEtaPhi()    
        # displayAll.viewEtaPhi()    


        try:
            input("Press enter to continue")
        except SyntaxError:
            pass


