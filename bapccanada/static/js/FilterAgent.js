'use strict';

const aRatingIds = ["star0", "star1", "star2", "star3", "star4"];
const sRangeId = "rangeSliderFilter";
const sDimensionCheckboxPrefix = "filterChoice";
const sAllCheckboxPrefix = "filterAllCheckBox";

export default class FilterAgent {
    constructor(oFilterMetadata) {
        // do initial setup
        this._filterMetadata = oFilterMetadata;
        this.initRatings();
        this.initPriceRanges();
        this.initDimensionModel();
    }

    initPriceRanges() {
        this.oRangeFilter = $(sRangeId)[0];
    }

    /**
     * rating metadata is optional parameter
     * if none was given to us, then we know it is a regular page load with no previous state
     */
    initRatings() {
        if (!this.getRatingMetadata()) {
            // no rating response from server, create default mapping without checking state
            const aRatings = aRatingIds.map((sRatingId) => {
                return {
                    "star_num": parseInt(sRatingId.substr(sRatingId.length - 1)),
                    "star_id": sRatingId,
                    "star_checkbox": FilterAgent.getJqueryObject(sRatingId)
                };
            });

            this.mRatings = new Map();
            aRatings.forEach((oRating) => {
                this.mRatings.set(oRating.star_id, oRating);
            })
        } else {
            // make sure to recheck appropriate checkboxes to match previous state
        }
    }

    initDimensionModel() {
        const oDimensionMetadata = this.getDimensionMetadata();

        if (oDimensionMetadata) {
            this.mDimensions = new Map();
            const aDimensionKeys = Object.keys(oDimensionMetadata);

            aDimensionKeys.forEach((sKey) => {
                const aDimensionEntries = $.extend(true, [], oDimensionMetadata[sKey]);

                aDimensionEntries.forEach((oDimensionEntry) => {
                    let sSelector = oDimensionEntry.checkbox_id;
                    if (oDimensionEntry.filter_value === "ALL") {
                        sSelector = sAllCheckboxPrefix + sSelector;
                    } else {
                        sSelector = sDimensionCheckboxPrefix + sSelector;
                    }

                    oDimensionEntry.value_checkbox = FilterAgent.getJqueryObject(sSelector);
                    oDimensionEntry.ui_dimension_name = sKey;
                    this.mDimensions.set(sSelector, oDimensionEntry);
                });
            });

            this.restoreCheckboxState(Array.from(this.mDimensions.keys()));
        }
    }

    /** Used to double check and restore state upon page reloads. Assumes models have been initiated prior to calling.
     *
     * @param aElementIds     array of checkboxes to check
     */
    restoreCheckboxState(aElementIds) {
        aElementIds.forEach((sElementId) => {
            const bChecked = this.mDimensions.get(sElementId).was_checked;
            if (bChecked) {
                const oElement = FilterAgent.getJqueryObject(sElementId);
                oElement.prop('checked', true);
            }
        })
    }

    getFilterMetadata() {
        return this._filterMetadata;
    }

    getDimensionMetadata() {
        return this._filterMetadata && this._filterMetadata.dimensions;
    }

    getRangeMetadata() {
        return this._filterMetadata && this._filterMetadata.ranges;
    }

    getRatingMetadata() {
        return this._filterMetadata && this._filterMetadata.ratings;
    }

    static getJqueryObject(sSelectorId) {
        return $("." + sSelectorId);
    }
}

