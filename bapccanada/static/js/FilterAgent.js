'use strict';

const aRatingIds = [".star0", ".star1", ".star2", ".star3", ".star4"];
const sRangeId = "rangeSliderFilter";

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

    initRatings() {
        if (!this.getRatingMetadata()) {
            const aRatings = aRatingIds.map((sRatingId) => {
                return {
                    "star_num": parseInt(sRatingId.substr(sRatingId.length - 1)),
                    "star_id": sRatingId,
                    "star_checkbox": $(sRatingId)[0]
                };
            });

            this.mRatings = new Map();
            aRatings.forEach((oRating) => {
                this.mRatings.set(oRating.star_num, oRating);
            })
        } else {

        }
    }

    initDimensionModel(oDimensionMetadata) {

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
}

