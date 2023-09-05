/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useModelField } from "@web/core/model_field_selector/model_field_hook";
import { useUniquePopover } from "@web/core/model_field_selector/unique_popover_hook";
import { ModelFieldSelectorPopover } from "@web/core/model_field_selector/model_field_selector_popover";

import { Component, onWillStart, onWillUpdateProps } from "@odoo/owl";
//import fieldRegistry from 'web.field_registry';
import config from 'web.config';
import fieldUtils from 'web.field_utils';

var AbstractField = require('web.AbstractField');
var Registry = require('web.field_registry');
var ModelFieldSelector = require("web.ModelFieldSelector");

export class ReportGetFieldModel extends Component {
//    static template = 'FieldReportField';
    setup() {
        this.popover = useUniquePopover();
        this.modelField = useModelField();
        this.chain = [];
        this.z_model = this._get_model();
        this.z_fieldName = this.props.value;

        onWillStart(async () => {
            this.chain = await this.loadChain(this.z_model, this.props.value);
        });
        onWillUpdateProps(async (nextProps) => {
            this.chain = await this.loadChain(nextProps.record.data.root_model_name, nextProps.record.data.model_field_selector);
        });
    }

    get fieldNameChain() {
        return this.getFieldNameChain(this.z_fieldName);
    }

    getFieldNameChain(fieldName) {
        return fieldName.length ? fieldName.split(".") : [];
    }

    async loadChain(resModel, fieldName) {
        if ("01".includes(fieldName)) {
            return [{ resModel, field: { string: fieldName } }];
        }
        const fieldNameChain = this.getFieldNameChain(fieldName);
        let currentNode = {
            resModel,
            field: null,
        };
        const chain = [currentNode];
        for (const fieldName of fieldNameChain) {
            const fieldsInfo = await this.modelField.loadModelFields(currentNode.resModel);
            Object.assign(currentNode, {
                field: { ...fieldsInfo[fieldName], name: fieldName },
            });
            if (fieldsInfo[fieldName].relation) {
                currentNode = {
                    resModel: fieldsInfo[fieldName].relation,
                    field: null,
                };
                chain.push(currentNode);
            }
        }
        return chain;
    }
    update(chain) {
        this.props.update(chain.join("."));
    }

    onFieldSelectorClick(ev) {
        if (this.props.readonly) {
            return;
        }
        this.popover.add(
            ev.currentTarget,
            this.constructor.components.Popover,
            {
                chain: this.chain,
                update: this.update.bind(this),
                showSearchInput: this.props.showSearchInput,
                isDebugMode: true,
                loadChain: this.loadChain.bind(this),
                filter: this.props.filter,
                followRelations: this.props.followRelations,
            },
            {
                closeOnClickAway: true,
                popoverClass: "o_popover_field_selector",
            }
        );
    }

//    async _get_field_name(){
//        FieldName = await this.modelField.loadModelFields(this.z_model)
//        return FieldName
//    }

    _get_model(){
        if(this.props.record.data.root_model_name){
            return this.props.record.data.root_model_name;
        }
    }
}
Object.assign(ReportGetFieldModel,{
    template: "FieldReportField",
    components: {
        Popover: ModelFieldSelectorPopover,
    },
//    props: {
//        fieldName: String,
//        resModel: String,
//        readonly: { type: Boolean, optional: true },
//        showSearchInput: { type: Boolean, optional: true },
//        isDebugMode: { type: Boolean, optional: true },
//        update: { type: Function, optional: true },
//        filter: { type: Function, optional: true },
//        followRelations: { type: Boolean, optional: true },
//    },
    defaultProps: {
        readonly: true,
        isDebugMode: true,
        showSearchInput: true,
        update: () => {},
        filter: () => true,
        followRelations: true,
    },
});
registry.category("fields").add("rp_field", ReportGetFieldModel);