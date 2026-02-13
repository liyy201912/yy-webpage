#!/usr/bin/env python3
"""Extract Yanyu Li's Google Scholar data from fetched HTML/JSON."""

import re
import json
import html

# Data extracted from the page
RESEARCHER = {
    "full_name": "Yanyu Li",
    "affiliation": "PhD, Northeastern University",
    "research_interests": ["Machine Learning"],
    "profile_photo_url": "https://scholar.googleusercontent.com/citations?view_op=medium_photo&user=XUj8koUAAAAJ&citpid=1",
    "citation_statistics": {
        "total_citations": 2806,
        "citations_since_2021": 2804,
        "h_index": 23,
        "i10_index": 32,
    },
}

# Publications from initial HTML (first 20)
PUBLICATIONS_HTML = """
1. Efficientformer: Vision transformers at mobilenet speed | Y Li, G Yuan, Y Wen, J Hu, G Evangelidis, S Tulyakov, Y Wang, J Ren | Advances in Neural Information Processing Systems 35, 12934-12949 | 2022 | 731
2. Rethinking vision transformers for mobilenet size and speed | Y Li, J Hu, Y Wen, G Evangelidis, K Salahi, Y Wang, S Tulyakov, J Ren | Proceedings of the IEEE/CVF international conference on computer vision | 2023 | 403
3. Snapfusion: Text-to-image diffusion model on mobile devices within two seconds | Y Li, H Wang, Q Jin, J Hu, P Chemerys, Y Fu, Y Wang, S Tulyakov, J Ren | Advances in Neural Information Processing Systems 36, 20662-20678 | 2023 | 284
4. Yolobile: Real-time object detection on mobile devices via compression-compilation co-design | Y Cai, H Li, G Yuan, W Niu, Y Li, X Tang, B Ren, Y Wang | Proceedings of the AAAI conference on artificial intelligence 35 (2), 955-963 | 2021 | 161
5. Mix and match: A novel fpga-centric deep neural network quantization framework | SE Chang, Y Li, M Sun, R Shi, HKH So, X Qian, Y Wang, X Lin | 2021 IEEE International Symposium on High-Performance Computer Architecture | 2021 | 156
6. Film-qnn: Efficient fpga acceleration of deep neural networks with intra-layer, mixed-precision quantization | M Sun, Z Li, A Lu, Y Li, SE Chang, X Ma, X Lin, Z Fang | Proceedings of the 2022 ACM/SIGDA International Symposium on Field | 2022 | 119
7. Auto-vit-acc: An fpga-aware automatic acceleration framework for vision transformer with mixed-scheme quantization | Z Li, M Sun, A Lu, H Ma, G Yuan, Y Xie, H Tang, Y Li, M Leeser, Z Wang | 2022 32nd International Conference on Field-Programmable Logic and | 2022 | 102
8. Pruning-as-search: Efficient neural architecture search via channel pruning and structural reparameterization | Y Li, P Zhao, G Yuan, X Lin, Y Wang, X Chen | IJCAI 2022 | 2022 | 76
9. Hyperhuman: Hyper-realistic human generation with latent structural diffusion | X Liu, J Ren, A Siarohin, I Skorokhodov, Y Li, D Lin, X Liu, Z Liu | arXiv preprint arXiv:2310.08579 | 2023 | 74
10. NPAS: A compiler-aware framework of unified network pruning and architecture search for beyond real-time mobile acceleration | Z Li, G Yuan, W Niu, P Zhao, Y Li, Y Cai, X Shen, Z Zhan, Z Kong, Q Jin | Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern | 2021 | 53
11. Compiler-aware neural architecture search for on-mobile real-time super-resolution | Y Wu, Y Gong, P Zhao, Y Li, Z Zhan, W Niu, H Tang, M Qin, B Ren | European Conference on Computer Vision, 92-111 | 2022 | 48
12. Lazydit: Lazy learning for the acceleration of diffusion transformers | X Shen, Z Song, Y Zhou, B Chen, Y Li, Y Gong, K Zhang, H Tan, J Kuen | Proceedings of the AAAI Conference on Artificial Intelligence 39 (19), 20409 | 2025 | 45
13. Pruning parameterization with bi-level optimization for efficient semantic segmentation on the edge | C Yang, P Zhao, Y Li, W Niu, J Guan, H Tang, M Qin, B Ren, X Lin | Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern | 2023 | 43
14. Bitsfusion: 1.99 bits weight quantization of diffusion model | Y Sui, Y Li, A Kag, Y Idelbayev, J Cao, J Hu, D Sagar, B Yuan, S Tulyakov | Advances in Neural Information Processing Systems 37, 76775-76818 | 2024 | 40
15. Improving the diffusability of autoencoders | I Skorokhodov, S Girish, B Hu, W Menapace, Y Li, R Abdal, S Tulyakov | arXiv preprint arXiv:2502.14831 | 2025 | 39
16. AirNN: Over-the-air computation for neural networks via reconfigurable intelligent surfaces | SG Sanchez, G Reus-Muns, C Bocanegra, Y Li, U Muncuk, Y Naderi | IEEE/ACM Transactions on Networking 31 (6), 2470-2482 | 2022 | 36
17. RMSMP: A novel deep neural network quantization framework with row-wise mixed schemes and multiple precisions | SE Chang, Y Li, M Sun, W Jiang, S Liu, Y Wang, X Lin | Proceedings of the IEEE/CVF international conference on computer vision | 2021 | 36
18. Layer freezing & data sieving: Missing pieces of a generic framework for sparse training | G Yuan, Y Li, S Li, Z Kong, S Tulyakov, X Tang, Y Wang, J Ren | Advances in Neural Information Processing Systems 35, 19061-19074 | 2022 | 34
19. Sf-v: Single forward video generation model | Z Zhang, Y Li, Y Wu, A Kag, I Skorokhodov, W Menapace, A Siarohin | Advances in Neural Information Processing Systems 37, 103599-103618 | 2024 | 29
20. Textcraftor: Your text encoder can be image quality controller | Y Li, X Liu, A Kag, J Hu, Y Idelbayev, D Sagar, Y Wang, S Tulyakov, J Ren | Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern | 2024 | 29
"""

def parse_publication_row(html_str):
    """Parse a publication from HTML row."""
    # Extract title
    title_match = re.search(r'class="gsc_a_at"[^>]*>([^<]+)</a>', html_str)
    title = html.unescape(title_match.group(1).strip()) if title_match else ""
    
    # Extract authors (first gs_gray div)
    authors_match = re.search(r'<div class="gs_gray">([^<]+)</div>', html_str)
    authors = html.unescape(authors_match.group(1).strip()) if authors_match else ""
    
    # Extract venue (second gs_gray div, before year)
    venue_match = re.search(r'<div class="gs_gray">[^<]+</div>\s*<div class="gs_gray">([^<]+)<span', html_str)
    if not venue_match:
        venue_match = re.search(r'<div class="gs_gray">[^<]+</div>\s*<div class="gs_gray">([^<]+)</div>', html_str)
    venue = html.unescape(venue_match.group(1).strip()) if venue_match else ""
    
    # Extract year
    year_match = re.search(r'<span class="gsc_a_h[^"]*"[^>]*>(\d{4})</span>', html_str)
    year = year_match.group(1) if year_match else ""
    
    # Extract citations
    cites_match = re.search(r'class="gsc_a_ac[^"]*"[^>]*>(\d*)</a>', html_str)
    citations = int(cites_match.group(1)) if cites_match and cites_match.group(1) else 0
    
    return {
        "title": title,
        "authors": authors,
        "venue": venue,
        "year": year,
        "citations": citations
    }

# Additional publications from API response (simplified - key ones)
ADDITIONAL_PUBS = [
    {"title": "Neural network-based OFDM receiver for resource constrained IoT devices", "authors": "N Soltani, H Cheng, M Belgiovine, Y Li, H Li, B Azari, S D'Oro, T Imbiriba", "venue": "IEEE Internet of Things Magazine 5 (3), 158-164", "year": "2022", "citations": 26},
    {"title": "EQ-ViT: Algorithm-hardware co-design for end-to-end acceleration of real-time vision transformer inference on Versal ACAP architecture", "authors": "P Dong, J Zhuang, Z Yang, S Ji, Y Li, D Xu, H Huang, J Hu, AK Jones", "venue": "IEEE Transactions on Computer-Aided Design of Integrated Circuits and", "year": "2024", "citations": 25},
    {"title": "Towards real-time segmentation on the edge", "authors": "Y Li, C Yang, P Zhao, G Yuan, W Niu, J Guan, H Tang, M Qin, Q Jin", "venue": "Proceedings of the AAAI conference on artificial intelligence 37 (2), 1468-1476", "year": "2023", "citations": 24},
    {"title": "E²GAN: Efficient Training of Efficient GANs for Image-to-Image Translation", "authors": "Y Gong, Z Zhan, Q Jin, Y Li, Y Idelbayev, X Liu, A Zharkov, K Aberman", "venue": "arXiv preprint arXiv:2401.06127", "year": "2024", "citations": 18},
    {"title": "Automated deep learning-based wide-band receiver", "authors": "B Azari, H Cheng, N Soltani, H Li, Y Li, M Belgiovine, T Imbiriba, S D'Oro", "venue": "Computer Networks 218, 109367", "year": "2022", "citations": 18},
    {"title": "Snapgen-v: Generating a five-second video within five seconds on a mobile device", "authors": "Y Wu, Z Zhang, Y Li, Y Xu, A Kag, Y Sui, H Coskun, K Ma, A Lebedev", "venue": "Proceedings of the Computer Vision and Pattern Recognition Conference, 2479-2490", "year": "2025", "citations": 17},
    {"title": "Snapgen: Taming high-resolution text-to-image models for mobile devices with efficient architectures and training", "authors": "J Chen, D Hu, X Huang, H Coskun, A Sahni, A Gupta, A Goyal, D Lahiri", "venue": "Proceedings of the Computer Vision and Pattern Recognition Conference, 7997-8008", "year": "2025", "citations": 17},
    {"title": "Sda: Low-bit stable diffusion acceleration on edge fpgas", "authors": "G Yang, Y Xie, ZJ Xue, SE Chang, Y Li, P Dong, J Lei, W Xie, Y Wang", "venue": "2024 34th International Conference on Field-Programmable Logic and", "year": "2024", "citations": 17},
]

# First 20 from HTML
PUBLICATIONS = [
    {"title": "Efficientformer: Vision transformers at mobilenet speed", "authors": "Y Li, G Yuan, Y Wen, J Hu, G Evangelidis, S Tulyakov, Y Wang, J Ren", "venue": "Advances in Neural Information Processing Systems 35, 12934-12949", "year": "2022", "citations": 731},
    {"title": "Rethinking vision transformers for mobilenet size and speed", "authors": "Y Li, J Hu, Y Wen, G Evangelidis, K Salahi, Y Wang, S Tulyakov, J Ren", "venue": "Proceedings of the IEEE/CVF international conference on computer vision", "year": "2023", "citations": 403},
    {"title": "Snapfusion: Text-to-image diffusion model on mobile devices within two seconds", "authors": "Y Li, H Wang, Q Jin, J Hu, P Chemerys, Y Fu, Y Wang, S Tulyakov, J Ren", "venue": "Advances in Neural Information Processing Systems 36, 20662-20678", "year": "2023", "citations": 284},
    {"title": "Yolobile: Real-time object detection on mobile devices via compression-compilation co-design", "authors": "Y Cai, H Li, G Yuan, W Niu, Y Li, X Tang, B Ren, Y Wang", "venue": "Proceedings of the AAAI conference on artificial intelligence 35 (2), 955-963", "year": "2021", "citations": 161},
    {"title": "Mix and match: A novel fpga-centric deep neural network quantization framework", "authors": "SE Chang, Y Li, M Sun, R Shi, HKH So, X Qian, Y Wang, X Lin", "venue": "2021 IEEE International Symposium on High-Performance Computer Architecture", "year": "2021", "citations": 156},
    {"title": "Film-qnn: Efficient fpga acceleration of deep neural networks with intra-layer, mixed-precision quantization", "authors": "M Sun, Z Li, A Lu, Y Li, SE Chang, X Ma, X Lin, Z Fang", "venue": "Proceedings of the 2022 ACM/SIGDA International Symposium on Field", "year": "2022", "citations": 119},
    {"title": "Auto-vit-acc: An fpga-aware automatic acceleration framework for vision transformer with mixed-scheme quantization", "authors": "Z Li, M Sun, A Lu, H Ma, G Yuan, Y Xie, H Tang, Y Li, M Leeser, Z Wang", "venue": "2022 32nd International Conference on Field-Programmable Logic and", "year": "2022", "citations": 102},
    {"title": "Pruning-as-search: Efficient neural architecture search via channel pruning and structural reparameterization", "authors": "Y Li, P Zhao, G Yuan, X Lin, Y Wang, X Chen", "venue": "IJCAI 2022", "year": "2022", "citations": 76},
    {"title": "Hyperhuman: Hyper-realistic human generation with latent structural diffusion", "authors": "X Liu, J Ren, A Siarohin, I Skorokhodov, Y Li, D Lin, X Liu, Z Liu", "venue": "arXiv preprint arXiv:2310.08579", "year": "2023", "citations": 74},
    {"title": "NPAS: A compiler-aware framework of unified network pruning and architecture search for beyond real-time mobile acceleration", "authors": "Z Li, G Yuan, W Niu, P Zhao, Y Li, Y Cai, X Shen, Z Zhan, Z Kong, Q Jin", "venue": "Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern", "year": "2021", "citations": 53},
    {"title": "Compiler-aware neural architecture search for on-mobile real-time super-resolution", "authors": "Y Wu, Y Gong, P Zhao, Y Li, Z Zhan, W Niu, H Tang, M Qin, B Ren", "venue": "European Conference on Computer Vision, 92-111", "year": "2022", "citations": 48},
    {"title": "Lazydit: Lazy learning for the acceleration of diffusion transformers", "authors": "X Shen, Z Song, Y Zhou, B Chen, Y Li, Y Gong, K Zhang, H Tan, J Kuen", "venue": "Proceedings of the AAAI Conference on Artificial Intelligence 39 (19), 20409", "year": "2025", "citations": 45},
    {"title": "Pruning parameterization with bi-level optimization for efficient semantic segmentation on the edge", "authors": "C Yang, P Zhao, Y Li, W Niu, J Guan, H Tang, M Qin, B Ren, X Lin", "venue": "Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern", "year": "2023", "citations": 43},
    {"title": "Bitsfusion: 1.99 bits weight quantization of diffusion model", "authors": "Y Sui, Y Li, A Kag, Y Idelbayev, J Cao, J Hu, D Sagar, B Yuan, S Tulyakov", "venue": "Advances in Neural Information Processing Systems 37, 76775-76818", "year": "2024", "citations": 40},
    {"title": "Improving the diffusability of autoencoders", "authors": "I Skorokhodov, S Girish, B Hu, W Menapace, Y Li, R Abdal, S Tulyakov", "venue": "arXiv preprint arXiv:2502.14831", "year": "2025", "citations": 39},
    {"title": "AirNN: Over-the-air computation for neural networks via reconfigurable intelligent surfaces", "authors": "SG Sanchez, G Reus-Muns, C Bocanegra, Y Li, U Muncuk, Y Naderi", "venue": "IEEE/ACM Transactions on Networking 31 (6), 2470-2482", "year": "2022", "citations": 36},
    {"title": "RMSMP: A novel deep neural network quantization framework with row-wise mixed schemes and multiple precisions", "authors": "SE Chang, Y Li, M Sun, W Jiang, S Liu, Y Wang, X Lin", "venue": "Proceedings of the IEEE/CVF international conference on computer vision", "year": "2021", "citations": 36},
    {"title": "Layer freezing & data sieving: Missing pieces of a generic framework for sparse training", "authors": "G Yuan, Y Li, S Li, Z Kong, S Tulyakov, X Tang, Y Wang, J Ren", "venue": "Advances in Neural Information Processing Systems 35, 19061-19074", "year": "2022", "citations": 34},
    {"title": "Sf-v: Single forward video generation model", "authors": "Z Zhang, Y Li, Y Wu, A Kag, I Skorokhodov, W Menapace, A Siarohin", "venue": "Advances in Neural Information Processing Systems 37, 103599-103618", "year": "2024", "citations": 29},
    {"title": "Textcraftor: Your text encoder can be image quality controller", "authors": "Y Li, X Liu, A Kag, J Hu, Y Idelbayev, D Sagar, Y Wang, S Tulyakov, J Ren", "venue": "Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern", "year": "2024", "citations": 29},
] + ADDITIONAL_PUBS

def main():
    output = {
        "researcher": RESEARCHER,
        "publications": PUBLICATIONS
    }
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
