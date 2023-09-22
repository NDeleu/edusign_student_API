from rest_framework.metadata import SimpleMetadata

class OrderingMetadata(SimpleMetadata):
    
    def determine_metadata(self, request, view):
        metadata = super().determine_metadata(request, view)
        
        # Add ordering information if available
        ordering_fields = getattr(view, 'ordering_fields', None)
        if ordering_fields:
            metadata['ordering'] = ordering_fields
        
        return metadata
