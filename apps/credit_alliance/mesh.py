def mesh_node(id, peers=5, firmware="custom"):
    return {"id":id, "peers":peers, "firmware":firmware, "status":"active", "protocols":["LoRa","WiFi-mesh","satellite-pallet"]}
def connect_mesh(nodes): return {"nodes":len(nodes), "resilience":min(1.0, len(nodes)/20), "decentralized":True}
