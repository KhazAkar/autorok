import enum

class SigrokCLIOptions(enum.Enum):
    Driver = '--driver'
    Verbose = '--verbose'
    Config = "--config"
    InputFile = "--input-format"
    OutputFile = "--output-file"
    OutputFormat = "--output-format"
    TransformModule = "--transform-module"
    ActiveChannels = "--channels"
    ChannelGroup = "--channel-group"
    Triggers = "--triggers"
    WaitForTrigger = "--wait-trigger"
    ProtocolDecoders = "--protocol-decoders"
    PDAnnotations = "--protocol-decoder-annotations"
    PDMeta = "--protocol-decoder-meta"
    PDBinary = "--protocol-decoder-binary"
    JsonTrace = "--protocol-decoder-jsontrace"
    ShowSampleNum = "--protocol-decoder-samplenum"
    Scan = "--scan"
    DontScan = "--dont-scan"
    ShowDetails = "--show"

class SampleMethod(enum.Enum):
    Continous = "--continous"
    Time = "--time"
    Samples = "--samples"
    Frames = "--frames"

class OutputFormats(enum.Enum):
    CSV = "csv"

class ProtocolDecoders(enum.Enum):
    UART = "uart"