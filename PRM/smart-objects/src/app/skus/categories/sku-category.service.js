"use strict";
var __extends = (this && this.__extends) || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
};
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var core_1 = require('@angular/core');
var http_1 = require('@angular/http');
var base_service_service_1 = require('../../utils/base-service.service');
var client_service_1 = require('../../clients/client.service');
var SkuCategoryService = (function (_super) {
    __extends(SkuCategoryService, _super);
    function SkuCategoryService(http) {
        _super.call(this, http);
    }
    SkuCategoryService.getSkuCategoriesUrl = function (idClient) {
        var urlClient = client_service_1.ClientService.getClientUrl(idClient);
        return "" + urlClient + SkuCategoryService.categoriesUrlPosfix;
    };
    SkuCategoryService.getSkuCategoryUrl = function (idClient, id) {
        return base_service_service_1.BaseService.getItemUrl(SkuCategoryService.getSkuCategoriesUrl(idClient), id);
    };
    SkuCategoryService.prototype.getSkuCategories = function (idClient) {
        return this.getCollection(SkuCategoryService.getSkuCategoriesUrl(idClient));
    };
    SkuCategoryService.prototype.getSkuCategory = function (idClient, id) {
        return this.getItem(SkuCategoryService.getSkuCategoriesUrl(idClient), id);
    };
    SkuCategoryService.prototype.saveSkuCategory = function (idClient, category) {
        return this.saveItem(SkuCategoryService.getSkuCategoriesUrl(idClient), category);
    };
    SkuCategoryService.categoriesUrlPosfix = 'sku-categories/';
    SkuCategoryService = __decorate([
        core_1.Injectable(), 
        __metadata('design:paramtypes', [http_1.Http])
    ], SkuCategoryService);
    return SkuCategoryService;
}(base_service_service_1.BaseService));
exports.SkuCategoryService = SkuCategoryService;
exports.SKU_CATEGORIES_SERVICES = [SkuCategoryService];
//# sourceMappingURL=sku-category.service.js.map