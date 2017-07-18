# Please set the region name to be fixed.
# If it is empty, it will not be fixed.
FIXED_REGION_NAME = ''

MIDDLEWARE_CLASSES += (
    'horizon.fixed_region_middleware.FixedRegionMiddleware',
)
