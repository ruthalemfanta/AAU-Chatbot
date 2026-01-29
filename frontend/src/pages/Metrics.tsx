import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { MetricCard } from "@/components/MetricCard";
import { StatusBadge } from "@/components/StatusBadge";
import { Textarea } from "@/components/ui/textarea";
import { useToast } from "@/hooks/use-toast";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import aauLogo from "@/assets/aau-logo.png";
import { apiService, type EvaluationResponse, type HealthResponse, type IntentsResponse } from "@/lib/api";
import {
  MessageSquare,
  ArrowLeft,
  GraduationCap,
  HeartPulse,
  ListChecks,
  Activity,
  Upload,
  Target,
  TrendingUp,
  BarChart3,
  RefreshCw,
} from "lucide-react";

// Sample test data for evaluation
const SAMPLE_TEST_DATA = [
  {
    text: "I want to apply for computer science admission",
    intent: "admission_inquiry",
    parameters: { department: ["computer science"] }
  },
  {
    text: "How do I register for second semester 2024?",
    intent: "registration_help",
    parameters: { semester: ["second"], year: ["2024"] }
  },
  {
    text: "I need to pay 5000 birr for tuition fees",
    intent: "fee_payment",
    parameters: { fee_amount: ["5000"] }
  },
  {
    text: "Can I get my transcript from engineering department?",
    intent: "transcript_request",
    parameters: { document_type: ["transcript"], department: ["engineering"] }
  },
  {
    text: "What are my grades for first semester 2023?",
    intent: "grade_inquiry",
    parameters: { semester: ["first"], year: ["2023"] }
  },
  {
    text: "Tell me about courses in business department",
    intent: "course_information",
    parameters: { department: ["business"] }
  },
  {
    text: "When is the class schedule for fall semester 2024?",
    intent: "schedule_inquiry",
    parameters: { semester: ["fall"], year: ["2024"] }
  },
  {
    text: "I need a degree certificate",
    intent: "document_request",
    parameters: { document_type: ["degree certificate"] }
  },
  {
    text: "Hello, I need help with AAU services",
    intent: "general_info",
    parameters: {}
  },
  {
    text: "I can't access my student portal",
    intent: "technical_support",
    parameters: {}
  }
];

export default function Metrics() {
  const { toast } = useToast();
  const [healthStatus, setHealthStatus] = useState<"healthy" | "loading" | "error">("loading");
  const [healthData, setHealthData] = useState<HealthResponse | null>(null);
  const [intentsData, setIntentsData] = useState<IntentsResponse | null>(null);
  const [trainingData, setTrainingData] = useState("");
  const [isTraining, setIsTraining] = useState(false);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [evaluationResult, setEvaluationResult] = useState<EvaluationResponse | null>(null);

  // Load initial data
  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      const [health, intents] = await Promise.all([
        apiService.getHealth(),
        apiService.getIntents()
      ]);
      
      setHealthData(health);
      setIntentsData(intents);
      setHealthStatus("healthy");
    } catch (error) {
      console.error("Failed to load initial data:", error);
      setHealthStatus("error");
      toast({
        title: "Connection Error",
        description: "Failed to connect to the chatbot API. Make sure the server is running.",
        variant: "destructive",
      });
    }
  };

  const handleHealthCheck = async () => {
    setHealthStatus("loading");
    try {
      const health = await apiService.getHealth();
      setHealthData(health);
      setHealthStatus("healthy");
      toast({
        title: "Health Check Passed",
        description: "All systems are operational.",
      });
    } catch (error) {
      setHealthStatus("error");
      toast({
        title: "Health Check Failed",
        description: "Unable to connect to the API server.",
        variant: "destructive",
      });
    }
  };

  const handleTrain = async () => {
    if (!trainingData.trim()) {
      toast({
        title: "No Training Data",
        description: "Please enter training data before submitting.",
        variant: "destructive",
      });
      return;
    }

    setIsTraining(true);
    try {
      const parsedData = JSON.parse(trainingData);
      const trainingArray = Array.isArray(parsedData) ? parsedData : [parsedData];
      
      const result = await apiService.trainModel({ training_data: trainingArray });
      
      setTrainingData("");
      toast({
        title: "Training Complete",
        description: `Model updated with ${result.samples_trained} samples.`,
      });
    } catch (error) {
      console.error("Training failed:", error);
      toast({
        title: "Training Failed",
        description: "Please check your training data format.",
        variant: "destructive",
      });
    } finally {
      setIsTraining(false);
    }
  };

  const handleEvaluate = async () => {
    setIsEvaluating(true);
    setEvaluationResult(null);
    
    try {
      const result = await apiService.evaluateModel(SAMPLE_TEST_DATA);
      setEvaluationResult(result);
      toast({
        title: "Evaluation Complete",
        description: `Evaluated ${result.total_samples} samples with ${(result.intent_accuracy * 100).toFixed(1)}% accuracy.`,
      });
    } catch (error) {
      console.error("Evaluation failed:", error);
      toast({
        title: "Evaluation Failed",
        description: "Unable to run model evaluation.",
        variant: "destructive",
      });
    } finally {
      setIsEvaluating(false);
    }
  };

  const getParameterColor = (value: number) => {
    if (value >= 0.9) return "text-green-600";
    if (value >= 0.8) return "text-yellow-600";
    return "text-red-600";
  };

  const getParameterVariant = (value: number): "default" | "secondary" | "destructive" => {
    if (value >= 0.9) return "default";
    if (value >= 0.8) return "secondary";
    return "destructive";
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link to="/">
              <Button variant="ghost" size="icon" className="mr-2">
                <ArrowLeft className="h-5 w-5" />
              </Button>
            </Link>
            <img src={aauLogo} alt="AAU Logo" className="w-8 h-8 object-contain" />
            <div>
              <h1 className="font-heading font-semibold">Metrics Dashboard</h1>
              <p className="text-xs text-muted-foreground">Monitor and evaluate your chatbot performance</p>
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={loadInitialData} className="gap-2">
              <RefreshCw className="h-4 w-4" />
              <span className="hidden sm:inline">Refresh</span>
            </Button>
            <Link to="/">
              <Button variant="outline" size="sm" className="gap-2">
                <MessageSquare className="h-4 w-4" />
                <span className="hidden sm:inline">Chat</span>
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto p-4 sm:p-6 space-y-6">
        {/* Quick Stats */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="bg-card rounded-xl p-4 border">
            <p className="text-xs text-muted-foreground">Total Intents</p>
            <p className="text-2xl font-heading font-semibold">
              {intentsData?.total_intents || 0}
            </p>
          </div>
          <div className="bg-card rounded-xl p-4 border">
            <p className="text-xs text-muted-foreground">Model Status</p>
            <p className="text-sm font-medium mt-1">
              {healthData?.nlp_engine_trained ? "Trained" : "Not Trained"}
            </p>
          </div>
          <div className="bg-card rounded-xl p-4 border">
            <p className="text-xs text-muted-foreground">Intent Accuracy</p>
            <p className="text-2xl font-heading font-semibold">
              {evaluationResult ? `${(evaluationResult.intent_accuracy * 100).toFixed(1)}%` : "N/A"}
            </p>
          </div>
          <div className="bg-card rounded-xl p-4 border">
            <p className="text-xs text-muted-foreground">System Status</p>
            <div className="mt-1">
              <StatusBadge status={healthStatus} />
            </div>
          </div>
        </div>

        {/* API Endpoints */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* Health Check */}
          <MetricCard
            title="System Health"
            description="GET /health - Check system status"
            icon={<HeartPulse className="h-5 w-5" />}
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <StatusBadge status={healthStatus} />
                <Button
                  onClick={handleHealthCheck}
                  variant="outline"
                  size="sm"
                  disabled={healthStatus === "loading"}
                >
                  {healthStatus === "loading" ? "Checking..." : "Run Check"}
                </Button>
              </div>
              {healthData && (
                <div className="text-xs text-muted-foreground space-y-1">
                  <p>Last check: {new Date(healthData.timestamp).toLocaleString()}</p>
                  <p>NLP Engine: {healthData.nlp_engine_trained ? "✅ Trained" : "❌ Not Trained"}</p>
                </div>
              )}
            </div>
          </MetricCard>

          {/* Performance Evaluation */}
          <MetricCard
            title="Model Evaluation"
            description="POST /evaluate - Run comprehensive evaluation"
            icon={<Activity className="h-5 w-5" />}
          >
            <div className="space-y-3">
              {evaluationResult && (
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Intent Accuracy</span>
                    <Badge variant="default">
                      {(evaluationResult.intent_accuracy * 100).toFixed(1)}%
                    </Badge>
                  </div>
                  <Progress value={evaluationResult.intent_accuracy * 100} className="h-2" />
                  <p className="text-xs text-muted-foreground">
                    Evaluated on {evaluationResult.total_samples} test samples
                  </p>
                </div>
              )}
              <Button onClick={handleEvaluate} disabled={isEvaluating} className="w-full">
                {isEvaluating ? "Evaluating..." : "Run Evaluation"}
              </Button>
            </div>
          </MetricCard>

          {/* Train Model */}
          <MetricCard
            title="Train Model"
            description="POST /train - Add new training data"
            icon={<GraduationCap className="h-5 w-5" />}
          >
            <div className="space-y-3">
              <Textarea
                placeholder='[{"text": "I want to apply for CS", "intent": "admission_inquiry", "parameters": {"department": ["computer science"]}}]'
                value={trainingData}
                onChange={(e) => setTrainingData(e.target.value)}
                className="min-h-[80px] font-mono text-xs"
              />
              <Button onClick={handleTrain} disabled={isTraining} className="w-full gap-2">
                <Upload className="h-4 w-4" />
                {isTraining ? "Training..." : "Submit Training Data"}
              </Button>
            </div>
          </MetricCard>

          {/* Supported Intents */}
          <MetricCard
            title="Supported Intents"
            description="GET /intents - List all supported intents"
            icon={<ListChecks className="h-5 w-5" />}
          >
            <div className="space-y-2 max-h-[200px] overflow-y-auto">
              {intentsData?.intents.map((intent) => (
                <div
                  key={intent}
                  className="flex items-center justify-between py-2 px-3 bg-muted/50 rounded-lg text-sm"
                >
                  <span className="font-mono text-xs">{intent}</span>
                  <Badge variant="outline" className="text-xs">
                    Active
                  </Badge>
                </div>
              )) || (
                <p className="text-sm text-muted-foreground">Loading intents...</p>
              )}
            </div>
          </MetricCard>
        </div>

        {/* Parameter Precision Metrics */}
        {evaluationResult && (
          <MetricCard
            title="Parameter Extraction Precision"
            description="Individual parameter evaluation metrics"
            icon={<Target className="h-5 w-5" />}
          >
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {Object.entries(evaluationResult.parameter_metrics).map(([param, metrics]) => (
                  <div key={param} className="p-4 border rounded-lg space-y-3">
                    <h4 className="font-medium text-sm capitalize">{param.replace('_', ' ')}</h4>
                    
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-xs text-muted-foreground">Precision</span>
                        <Badge variant={getParameterVariant(metrics.precision)} className="text-xs">
                          {(metrics.precision * 100).toFixed(1)}%
                        </Badge>
                      </div>
                      <Progress value={metrics.precision * 100} className="h-1.5" />
                      
                      <div className="flex justify-between items-center">
                        <span className="text-xs text-muted-foreground">Recall</span>
                        <Badge variant={getParameterVariant(metrics.recall)} className="text-xs">
                          {(metrics.recall * 100).toFixed(1)}%
                        </Badge>
                      </div>
                      <Progress value={metrics.recall * 100} className="h-1.5" />
                      
                      <div className="flex justify-between items-center">
                        <span className="text-xs text-muted-foreground">F1-Score</span>
                        <Badge variant={getParameterVariant(metrics.f1)} className="text-xs">
                          {(metrics.f1 * 100).toFixed(1)}%
                        </Badge>
                      </div>
                      <Progress value={metrics.f1 * 100} className="h-1.5" />
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="mt-4 p-3 bg-muted/30 rounded-lg">
                <h5 className="text-sm font-medium mb-2 flex items-center gap-2">
                  <BarChart3 className="h-4 w-4" />
                  Performance Targets
                </h5>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-2 text-xs">
                  <div>Department: &gt;90%</div>
                  <div>Semester: &gt;85%</div>
                  <div>Year: &gt;95%</div>
                  <div>Document: &gt;90%</div>
                  <div>Fee Amount: &gt;85%</div>
                </div>
              </div>
            </div>
          </MetricCard>
        )}
      </main>
    </div>
  );
}
