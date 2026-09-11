(ns kawase-yui.murakumo-test
  (:require [clojure.test :refer [deftest is testing]]
            [kawase-yui.murakumo :as kawase]))

(def full-attestations
  (into {}
        (map (fn [gate] [gate (str "attested-" (name gate))]))
        (distinct (mapcat :required-gates (vals kawase/cell-specs)))))

(deftest maps-all-legacy-kawase-cells
  (is (= #{"kawase_fx_oracle_watcher"
           "kawase_jurisdiction_compliance"
           "kawase_pool_match"
           "kawase_rebalance_proposer"
           "kawase_silen_review"}
         (set (map :legacy-cell (vals kawase/cell-specs))))))

(deftest r0-gates-block-effects
  (let [plan (kawase/cell-plan :pool-match
                               {:intent-cid "bafkreiintent"
                                :sender-did "did:example:alice"
                                :recipient-did "did:example:bob"
                                :computed-at "2026-06-29T00:00:00Z"})]
    (is (= :blocked (:status plan)))
    (is (= [:council-charter-attestation
            :silen-kawase-baseline-review
            :charter-rider-scan-baseline
            :kotoba-attestation-lineage-baseline
            :adherent-sbt-baseline
            :mid-market-chainlink-band-baseline
            :zero-spread-profit-baseline
            :stable-only-pool-baseline
            :no-commercial-remittance-msb-baseline
            :no-fiat-custody-baseline
            :per-month-cap-baseline
            :kyc-is-adherent-sbt-baseline
            :no-chargeback-baseline
            :murakumo-only-inference-baseline
            :kotoba-only-substrate-baseline
            :jurisdiction-council-lv7-unanimity-baseline
            :sender-adherent-sbt-baseline
            :recipient-adherent-sbt-baseline
            :prefunded-pool-baseline
            :deposit-claim-only-baseline
            :intent-cid-baseline]
           (:missing-gates plan)))
    (is (empty? (:effects plan)))))

(deftest pool-match-emits-three-attested-records
  (let [plan (kawase/cell-plan :pool-match
                               {:attestations full-attestations
                                :intent-cid "bafkreiintent"
                                :sender-did "did:example:alice"
                                :recipient-did "did:example:bob"
                                :source-stable "USDC"
                                :target-stable "EURC"
                                :source-amount-minor 10000000
                                :target-amount-minor 9200000
                                :fx-rate-bps 9200
                                :computed-at "2026-06-29T00:00:00Z"})
        collections (map :collection (:effects plan))]
    (is (= :ready (:status plan)))
    (is (= ["com.etzhayyim.kawase.depositAttestation"
            "com.etzhayyim.kawase.withdrawIntent"
            "com.etzhayyim.kawase.matchExecution"]
           collections))
    (is (every? #(= 0 (get-in % [:record :spreadProfitMkoto])) (:effects plan)))
    (is (every? #(true? (get-in % [:record :stableOnly])) (:effects plan)))))

(deftest fx-oracle-enforces-mid-market-band-attestation
  (let [attestations (dissoc full-attestations :max-band-bps-50-baseline)
        plan (kawase/cell-plan :fx-oracle-watcher
                               {:attestations attestations
                                :fx-rate-attestation-cid "bafkreifx"})]
    (is (= :blocked (:status plan)))
    (is (= [:max-band-bps-50-baseline] (:missing-gates plan)))))

(deftest jurisdiction-cell-is-sole-pair-activation-gate
  (let [attestations (dissoc full-attestations :lv7-unanimity-per-pair-baseline)
        plan (kawase/cell-plan :jurisdiction-compliance
                               {:attestations attestations
                                :jurisdiction-pair "USA-EUR"})]
    (is (= :blocked (:status plan)))
    (is (= [:lv7-unanimity-per-pair-baseline] (:missing-gates plan)))))

(deftest rebalance-proposer-rejects-yield-and-lp-paths
  (let [attestations (-> full-attestations
                         (dissoc :no-defi-yield-baseline)
                         (dissoc :no-lp-position-baseline))
        plan (kawase/cell-plan :rebalance-proposer
                               {:attestations attestations
                                :rebalance-id "rebalance-001"})]
    (is (= :blocked (:status plan)))
    (is (= [:no-defi-yield-baseline :no-lp-position-baseline]
           (:missing-gates plan)))))

(deftest silen-review-keeps-forbidden-counters-zero
  (let [plan (kawase/cell-plan :silen-review
                               {:attestations full-attestations
                                :review-id "review-2026"
                                :computed-at "2026-06-29T00:00:00Z"})
        effect (first (:effects plan))]
    (is (= :ready (:status plan)))
    (is (= "com.etzhayyim.kawase.silenKawaseReview" (:collection effect)))
    (is (= 0 (get-in effect [:record :spreadProfitMkoto])))
    (is (= 0 (get-in effect [:record :commercialRemittanceIntegrationCount])))
    (is (= 0 (get-in effect [:record :fiatCustodyCount])))
    (is (= 0 (get-in effect [:record :chargebackCount])))))

(deftest all-cell-plans-ready-when-attested
  (let [plans (kawase/all-cell-plans {:attestations full-attestations
                                      :intent-cid "bafkreiintent"
                                      :sender-did "did:example:alice"
                                      :recipient-did "did:example:bob"
                                      :source-stable "USDC"
                                      :target-stable "EURC"
                                      :source-amount-minor 10000000
                                      :target-amount-minor 9200000
                                      :fx-rate-bps 9200
                                      :fx-rate-attestation-cid "bafkreifx"
                                      :jurisdiction-pair "USA-EUR"
                                      :pool-id "usdc-eurc-r1"
                                      :rebalance-id "rebalance-001"
                                      :review-id "review-2026"
                                      :computed-at "2026-06-29T00:00:00Z"})]
    (is (= (set (keys kawase/cell-specs)) (set (keys plans))))
    (is (every? #(= :ready (:status %)) (vals plans)))
    (is (= 8 (count (mapcat :effects (vals plans)))))))
