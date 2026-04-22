import { useState, useMemo } from "react";
import api from "../api/api";
import { useAuth } from "../context/useAuth";

export type Estimate = {
    id: number;
    customer_name: string;
    vehicle_model: string;
    repair_description: string;
    description: string;
    vehicle_year: number;
    vehicle_mileage: number;
    estimated_cost: number;
    status: string;
};

export const useEstimates = () => {
    const { token } = useAuth();
    const [estimates, setEstimates] = useState<Estimate[]>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const [statusFilter, setStatusFilter] = useState<string>("");

    const headers = useMemo(() => {
    return {
        Authorization: `Bearer ${token}`,
    };
    }, [token]);

    const createEstimate = async (estimateData) => {
        try {
            setError(null);
            const response = await api.post("/estimates", estimateData, { headers });
            setEstimates((prev) => [...prev, response.data]);
        } catch (error) {
            setError("Error creating estimate");
            console.error("Create estimate error:", error);
        }
    };

    const fetchEstimates = async () => {
        try{
            setLoading(true);
            setError(null);

            const response = await api.get("/estimates", { headers });
            setEstimates(response.data);
        } catch (error) {
            setError("Error fetching estimates");
            console.error("Fetch estimates error:", error);
        } finally {
            setLoading(false);
        }
    };

    return {
        estimates,
        loading,
        error,
        statusFilter,
        setStatusFilter,
        createEstimate,
        fetchEstimates,
    };
};