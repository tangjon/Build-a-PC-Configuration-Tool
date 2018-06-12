export default function prepareMetadataForAgent(oDimensionMetadata, oRangeMetadata, oRatingMetadata) {
    return {
        dimensions: oDimensionMetadata,
        ranges: oRangeMetadata,
        ratings: oRatingMetadata
    };
}